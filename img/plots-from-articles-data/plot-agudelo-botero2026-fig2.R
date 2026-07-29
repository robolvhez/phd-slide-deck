# ponytail: minimal script, no abstractions
library(tidyverse)

d <- read_csv("img/plots-from-articles-data/agudelo-botero2026-fig2-national-asmr.csv") |>
  pivot_longer(-year, names_to = "disease", values_to = "asmr") |>
  mutate(disease = case_match(disease,
    "heart_disease"      ~ "Enfermedad cardíaca",
    "stroke"             ~ "Enfermedad cerebrovascular",
    "diabetes_mellitus"  ~ "Diabetes mellitus",
    "hypertension"       ~ "Hipertensión"
  ))

pal <- c(
  "Enfermedad cardíaca"         = "#E63946",
  "Diabetes mellitus"           = "#457B9D",
  "Enfermedad cerebrovascular"  = "#F4A261",
  "Hipertensión"                = "#2A9D8F"
)

p <- ggplot(d, aes(year, asmr, colour = disease)) +
  annotate(
    "rect",
    xmin = 2020.5, xmax = 2024.5,
    ymin = 80, ymax = 148.5,
    color = "#E63946", fill = NA,
    linetype = "dashed", size = 1
  ) +
  ## annotate(
  ##   "text",
  ##   x = 1998, y = 142,
  ##   label = "Principales causas",
  ##   hjust = 0, vjust = 1,
  ##   fontface = "italic", color = "#721c24", size = 4
  ## ) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2.5) +
  geom_text(
    data = d |> filter(year == min(year)),
    aes(label = disease, vjust = ifelse(disease == "Diabetes mellitus", 2, -1)),
    hjust = 0,
    fontface = "bold",
    show.legend = FALSE,
    size = 4
  ) +
  geom_text(
    data = d |> filter(year == max(year)),
    aes(label = round(asmr, 1)),
    hjust = -0.3,
    fontface = "bold",
    show.legend = FALSE,
    size = 4
  ) +
  scale_colour_manual(values = pal) +
  scale_x_continuous(breaks = seq(1998, 2022, 4), expand = expansion(mult = c(0.05, 0.12))) +
  labs(
    x        = "Año",
    y        = "Mortalidad estandarizada por edad\n(muertes por cada 100,000 hab.)",
    colour   = NULL
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position  = "none",
    panel.grid.minor = element_blank()
  )

ggsave("img/plots-from-articles-data/agudelo-botero2026-fig2-national-asmr.pdf",
       p, width = 8, height = 4.5)
ggsave("img/plots-from-articles-data/agudelo-botero2026-fig2-national-asmr.png",
       p, width = 8, height = 4.5, dpi = 300)
