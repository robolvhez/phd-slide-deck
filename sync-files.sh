#!/bin/bash
#
# sync-files.sh — Synchronise (push) changes from the local
# articles directory to the Google Drive mirror.
#
# Usage:
#   ./sync-files.sh           # normal sync
#   ./sync-files.sh --dry-run # preview only, no changes written
#
# Safety features:
#   • Mounts Google Drive via rclone and unmounts on exit
#   • Validates both source and destination exist before running
#   • Excludes .git, __pycache__, and this script itself
#   • Dry-run mode for previewing changes
#   • Logs every run with timestamps
#   • Requires confirmation when --delete would remove files
# ----------------------------------------------------------------

set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
LOCAL="$SCRIPT_DIR/"
GDRIVE_MOUNT="$HOME/GoogleDrive"
GDRIVE="$GDRIVE_MOUNT/01_research-project/03_presentations/phd-slide-deck_latex/"
RCLONE_REMOTE="GDrive:"
LOGFILE="$HOME/.local/share/sync-articles.log"
WE_MOUNTED=false

# ── Colours (disabled when stdout is not a terminal) ─────────────
if [[ -t 1 ]]; then
    RED='\033[0;31m'   GREEN='\033[0;32m'
    YELLOW='\033[0;33m' BLUE='\033[0;34m'
    BOLD='\033[1m'      RESET='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' BOLD='' RESET=''
fi

# ── Helpers ──────────────────────────────────────────────────────
log()  { echo -e "${GREEN}[INFO]${RESET}  $*"; }
warn() { echo -e "${YELLOW}[WARN]${RESET}  $*" >&2; }
err()  { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

# ── Google Drive mount / unmount ─────────────────────────────────
mount_gdrive() {
    if mountpoint -q "$GDRIVE_MOUNT"; then
        log "Google Drive already mounted at ${BOLD}$GDRIVE_MOUNT${RESET}"
        return 0
    fi

    log "Mounting Google Drive → ${BOLD}$GDRIVE_MOUNT${RESET}"
    mkdir -p "$GDRIVE_MOUNT"
    rclone mount --vfs-cache-mode writes --daemon "$RCLONE_REMOTE" "$GDRIVE_MOUNT"

    # Wait for the mount to become available (up to 15 s)
    local retries=30
    while ! mountpoint -q "$GDRIVE_MOUNT"; do
        (( retries-- )) || { err "Timed out waiting for rclone mount."; exit 1; }
        sleep 0.5
    done

    WE_MOUNTED=true
    log "Google Drive mounted successfully."
}

unmount_gdrive() {
    if $WE_MOUNTED && mountpoint -q "$GDRIVE_MOUNT"; then
        log "Unmounting Google Drive…"
        fusermount3 -uz "$GDRIVE_MOUNT" 2>/dev/null \
            || umount "$GDRIVE_MOUNT" 2>/dev/null \
            || warn "Could not unmount $GDRIVE_MOUNT — please unmount manually."
    fi
}

# ── Parse arguments ──────────────────────────────────────────────
DRY_RUN=false
for arg in "$@"; do
    case "$arg" in
        --dry-run|-n) DRY_RUN=true ;;
        --help|-h)
            sed -n '2,/^# -/{ /^# -/!s/^# \?//p }' "$0"
            exit 0
            ;;
        *)
            { err "Unknown option: $arg (use --help for usage)"; exit 1; }
            ;;
    esac
done

# ── Pre-flight checks ───────────────────────────────────────────
[[ -d "$LOCAL" ]]  || { err "Source directory not found: $LOCAL"; exit 1; }

command -v rsync  &>/dev/null || { err "'rsync' is not installed."; exit 1; }
command -v rclone &>/dev/null || { err "'rclone' is not installed."; exit 1; }

# ── Mount Google Drive (unmount on exit) ─────────────────────────
mount_gdrive
trap unmount_gdrive EXIT

[[ -d "$GDRIVE" ]] || { err "Destination directory not found: $GDRIVE"; exit 1; }

# ── Build rsync options ─────────────────────────────────────────
RSYNC_OPTS=(
    -av
    --delete
    --exclude='.git/'
    --exclude='__pycache__/'
    --exclude='*.pyc'
    --exclude='sync-files.sh'
    --exclude='.DS_Store'
)

# ── Dry-run / deletion safety check ─────────────────────────────
if $DRY_RUN; then
    log "Dry-run mode — no files will be modified."
    RSYNC_OPTS+=(--dry-run)
else
    # Preview deletions and ask for confirmation
    DELETIONS=$(rsync -avn --delete \
        "${RSYNC_OPTS[@]/#-av/}" \
        "$LOCAL" "$GDRIVE" 2>/dev/null \
        | grep '^deleting ' || true)

    if [[ -n "$DELETIONS" ]]; then
        warn "The following files will be ${RED}DELETED${RESET} from the destination:"
        echo "$DELETIONS" | sed 's/^deleting /  ✗ /'
        echo ""
        read -rp "Continue? [y/N] " confirm
        case "$confirm" in
            [yY]|[yY][eE][sS]) ;;
            *) log "Aborted by user."; exit 0 ;;
        esac
    fi
fi

# ── Sync ─────────────────────────────────────────────────────────
log "Syncing: ${BOLD}$LOCAL${RESET} → ${BOLD}$GDRIVE${RESET}"

if rsync "${RSYNC_OPTS[@]}" "$LOCAL" "$GDRIVE"; then
    log "Sync completed successfully."
    # Append to log file
    mkdir -p "$(dirname "$LOGFILE")"
    echo "[$(timestamp)] OK  src=$LOCAL dst=$GDRIVE dry_run=$DRY_RUN" >> "$LOGFILE"
else
    EXIT_CODE=$?
    err "rsync exited with code $EXIT_CODE"
    mkdir -p "$(dirname "$LOGFILE")"
    echo "[$(timestamp)] FAIL(rc=$EXIT_CODE) src=$LOCAL dst=$GDRIVE" >> "$LOGFILE"
    exit $EXIT_CODE
fi
