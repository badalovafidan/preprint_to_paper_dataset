# tidyverse package allows for data manipulation and creating graphics via ggplot2  
library(tidyverse)

# cowplot library for arranging multipanel plots
library(cowplot)

# psych package containts cohen.kappa() function that is used to calcaute Cohen's kappa coefficent
library(psych)

# caret package for handling the traning and validation by logistic regression 
library(caret)

# set large timeout for reading in the main dataset
options(timeout = 600)


# Read in the annotation dataset
data.annotation <- read.csv("https://zenodo.org/records/17185408/files/PreprintToPaper_GrayZone.csv")


# Calculate Cohen's kappa
kappa <- data.annotation %>% 
  select(annotator1, annotator2) %>% 
  cohen.kappa()

print(kappa)

# Merge of annotations by conjuction
# cast type to factor
data.annotation <- data.annotation %>% 
  mutate(merged = annotator1 & annotator2)

# set parameters: 10-fold cross-validation
fit <- trainControl(method = "cv", number = 10)

# perform logistic regression of merged annotations versus author match score for non NA annotation
# merged annotations need to cast to factor
lm <- data.annotation %>% 
  filter(!is.na(merged)) %>%
  mutate(merged = factor(merged)) %>%
  train(merged ~ author_match_score, data = ., trControl = fit, method = "glm", family = "binomial")

# print accuracy and Cohen's kappa for logistic regression with their standrd deviations
print(lm$results)

# obtain logistic regression coefficents
coefficients <- summary(lm)$coefficients

# extract beta0 and beta1 coefficients with their uncertanities
beta0 <- round(coefficients[[1]], 2)
beta0.err <- round(coefficients[1,2], 2)

beta1 <- round(coefficients[[2]], 2)
beta1.err <- round(coefficients[2,2], 2)

# calculate location parameter
mu <- round(-beta0 / beta1, 2)

# calculate location parameter uncertanity using uncertanity propagation
mu.err <- round(sqrt((1/beta1)^2*beta0.err + (beta0/beta1^2)^2*beta1.err), 2)


# logistic regression function for plotting
lmfun <- function(x) 1.0 / (1.0 + exp(-(beta0 + beta1 * x)))


# use ggplot2 library to create a plot the merged annotations versus author match score
# along with the results from logistic regression
# data points are jittred to avoid overlap
g1 <- data.annotation %>%
  ggplot() + 
  geom_jitter(aes(x = author_match_score, y = as.numeric(merged)), 
              height = 0.05, size = 1.5, alpha=0.4, color = "black") + 
  geom_function(fun = lmfun, color = "orange", linewidth = 1) +
  scale_y_continuous(name = "combined annotations", breaks = c(0, 1), labels = c("FALSE", "TRUE")) +
  scale_x_continuous(name = "author match score")

# read in the main data file and extract only the publication status, preprint submission date and
# author match core
data.main <- read.csv("https://zenodo.org/records/17185408/files/PreprintToPaper.csv") %>%
  select(custom_status, biorxiv_submission_date_1st, author_match_score)

# extract the year of preprint submission (year column), 
# apply author match score threshold (equal to logistic regression location parameter) to distinguish
# between the published and preprint only papers (status corrected column),
# change the column name for papers not distinguishing preprint only and published among the gray zone group (status uncorrected column)
# 

data <- data.main %>% 
  transmute(year = year(as.Date(biorxiv_submission_date_1st, "%m/%d/%Y")), 
         status_corrected = ifelse(author_match_score > mu, "published", "preprint only"), 
         status_uncorrected = custom_status) %>%
  mutate(status_corrected = coalesce(status_corrected, status_uncorrected))


# calculate fractions of published papers without (fraction_uncorrected)
# or with (fraction_corrected) distinguishing preprint only and published among
# the gray zone group

fraction.stats <- data %>% 
  group_by(year) %>% 
  summarise(fraction_uncorrected = sum(status_uncorrected == "published") /n(), 
            fraction_corrected = sum(status_corrected == "published") / n())

# change the wide format into the long one for easier plot creation
fraction.stats.long <- fraction.stats %>% 
  pivot_longer(cols = fraction_uncorrected:fraction_corrected)


# create the plot of fraction of published papers versus the prepprint submission year
# for uncorrected and corrected group
g2 <- fraction.stats.long %>%
  ggplot() + 
  geom_point(aes(x = year, y = value, shape = name), size = 3) + 
  scale_y_continuous(name = "fraction of published papers", limits = c(0,.8), breaks = c(0, 0.25, 0.5, 0.75)) +
  scale_x_continuous(name = "year of preprint submission", breaks = c(2016, 2017, 2018, 2020, 2021, 2022)) +
  theme(panel.grid.minor = element_blank(), legend.position = "none")

# plot 
plot_grid(g1, g2, labels = c('a', 'b'))
