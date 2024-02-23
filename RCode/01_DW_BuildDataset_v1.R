# Author: M.L.


# end

library(dplyr)
library(plm)
library(readxl)
library(tidyverse)

## AR tendency df
df.AR.CPT.Tendency <- read.csv("Data/Agri_CPT_AR_2ndRound.csv") %>% na.omit()
df.AR.CPT.Tendency$DID <- gsub(".*\\b(\\d+)\\.pdf", "\\1", df.AR.CPT.Tendency$nake_name) %>% 
  as.integer()
df.AR.CPT.Tendency <- df.AR.CPT.Tendency %>%
  distinct(DID, .keep_all = TRUE)

## AR name and company
df.AR.name.Company.name <- read.csv("Data/FoodAndBeveragesCompanyNameCodeDID.csv") %>%
  dplyr::select(-X)
df.AR.name.Company.name <- df.AR.name.Company.name %>% distinct()
df.AR.name.Company.name <- df.AR.name.Company.name %>% rename('DID' = 'DCN')
#df.AR.name.Company.name <- df.AR.name.Company.name %>% filter(X0 != '') %>%
#  dplyr::select(X0, X1, X4, X6, X7, X8)
#colnames(df.AR.name.Company.name) <- c("company_name", "raw_code",
#                                       "DocYear", "Country",
#                                       "Industry", "DID")

## get company name and code
merged.df <- left_join(df.AR.CPT.Tendency, df.AR.name.Company.name, by = "DID")
merged.df$doc_year <- as.integer(substr(merged.df$Document_Date, 1, 4))
merged.df$doc_month <- as.integer(substr(merged.df$Document_Date, 6, 7))
merged.df <- merged.df %>%
  mutate(year = ifelse(doc_month>9, doc_year, doc_year-1))

## obtain the variable from Eikon
df.eikon.1 <- read_xlsx('Data/FoodAndBeveragesCompanyCode.xlsx') 
df.eikon.1 <- df.eikon.1[,4:ncol(df.eikon.1)]
colnames(df.eikon.1) <- c("Code", "FY", 'ROA', 'ROE', 'TotalAssets', 'MarketCapital',
                          'TotalDebt', 'TotalRevenue')
df.eikon.1$year <- as.integer(substr(df.eikon.1$FY, 3, 6))
df.eikon.1 <- df.eikon.1 %>% na.omit()

df.eikon.1$ROA <- df.eikon.1$ROA %>% as.numeric()
df.eikon.1$ROE <- df.eikon.1$ROE %>% as.numeric()
df.eikon.1$TotalAssets <- df.eikon.1$TotalAssets %>% as.numeric()
df.eikon.1$MarketCapital <- df.eikon.1$MarketCapital %>% as.numeric()
df.eikon.1$TotalDebt <- df.eikon.1$TotalDebt %>% as.numeric()
df.eikon.1$TotalRevenue <- df.eikon.1$TotalRevenue %>% as.numeric()


#df.eikon.2 <- read_xlsx('Data/VariableDownloadUse.xlsx', sheet = 'Sheet3')
#colnames(df.eikon.2) <- c("Code", "FY", 'EBTM', 'BoardSize', 'BoardGenderDiversity', 'BoardCulturalDiversity',
#                          'FreeFloat', 'totalLiabilities', 'CeoChairman')
#df.eikon.2 <- df.eikon.2 %>% 
#  filter(BoardSize != "Unable to collect data for the field 'TR.CGBoardSize' and some specific identifier(s).")
#df.eikon.2 <- df.eikon.2 %>% 
#  filter(FY != 'NULL')
#df.eikon.2$EBTM <- df.eikon.2$EBTM %>% as.numeric()
#df.eikon.2$BoardSize <- df.eikon.2$BoardSize %>% as.numeric()
#df.eikon.2$BoardGenderDiversity <- df.eikon.2$BoardGenderDiversity %>% as.numeric()
#df.eikon.2$BoardCulturalDiversity <- df.eikon.2$BoardCulturalDiversity %>% as.numeric()
#df.eikon.2$FreeFloat <- df.eikon.2$FreeFloat %>% as.numeric()
#df.eikon.2$totalLiabilities <- df.eikon.2$totalLiabilities %>% as.numeric()

#df.eikon <- left_join(df.eikon.1, df.eikon.2, by = c('Code', "FY"))

#df.eikon$year <- sub("^FY", "", df.eikon$FY) %>% as.integer()

## final dataset
merged.df <- left_join(merged.df, df.eikon.1, by = c('Code', 'year'))

## test
formula <-
  ROA ~ model_i0_index + model_i1_index + model_i2_index + model_i3_index +
  model_i4_index + model_i5_index + model_i6_index + model_i7_index +
  model_i8_index + model_i9_index + model_i10_index + model_i11_index + model_i12_index 
reg.result <- lm(formula, merged.df)
summary(reg.result)
within.result <- plm(formula, merged.df, effect = 'individual',
                         model = 'within', index = c('Code', 'year'))
summary(within.result)
random.result <- plm(formula, merged.df, effect = 'random',
                         model = 'within', index = c('Code', 'year'))
summary(random.result)


formula <-
  ROE ~ model_i0_index + model_i1_index + model_i2_index + model_i3_index +
  model_i4_index + model_i5_index + model_i6_index + model_i7_index +
  model_i8_index + model_i9_index + model_i10_index + model_i11_index + model_i12_index 
reg.result <- lm(formula, merged.df)
summary(reg.result)
within.result <- plm(formula, merged.df, effect = 'individual',
                     model = 'within', index = c('Code', 'year'))
summary(within.result)
random.result <- plm(formula, merged.df, effect = 'individual',
                     model = 'within', index = c('Code', 'year'))
summary(random.result)

formula <-
  TotalRevenue ~ model_i0_index + model_i1_index + model_i2_index + model_i3_index +
  model_i4_index + model_i5_index + model_i6_index + model_i7_index +
  model_i8_index + model_i9_index + model_i10_index + model_i11_index + model_i12_index 
reg.result <- lm(formula, merged.df)
summary(reg.result)
within.result <- plm(formula, merged.df, effect = 'individual',
                     model = 'within', index = c('Code', 'year'))
summary(within.result)
random.result <- plm(formula, merged.df, effect = 'individual',
                     model = 'within', index = c('Code', 'year'))
summary(random.result)


library(randomForest)
formula <-
  ROE ~ model_i0_index + model_i1_index + model_i2_index + model_i3_index +
  model_i4_index + model_i5_index + model_i6_index + model_i7_index +
  model_i8_index + model_i9_index + model_i10_index + model_i11_index + model_i12_index 
selected_columns <- all.vars(formula)
test_df_rf <- test_df %>%
  dplyr::select(all_of(selected_columns)) %>% na.omit()

rf_model <- randomForest(formula, data = test_df_rf, ntree=50)
print(rf_model)




