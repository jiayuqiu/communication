library(ggplot2)
library(ggmap)
library(data.table)
library(maps)

# 获取全球地图图层
mapWorld <- borders("world", colour="gray50", fill="gray50")
mp <- ggplot() + mapWorld

# 获取作图数据
ais_df = fread("/home/qiu/Documents/sisi2017/xukai_data/4ship_ais/4ship_ais_201703_paint.csv")
ais_df = ais_df[order(ais_df$unique_ID, ais_df$acquisition_time), ]
ais_df$longitude <- as.numeric(ais_df$longitude)
ais_df$latitude <- as.numeric(ais_df$latitude)

# 分船获取数据
ship1_357780000 <- ais_df[ais_df$unique_ID==357780000, ]
ship2_370016000 <- ais_df[ais_df$unique_ID==370016000, ]
ship3_219882000 <- ais_df[ais_df$unique_ID==219882000, ]
ship4_372278000 <- ais_df[ais_df$unique_ID==372278000, ]

# 获取标注的坐标
ship1_357780000_coor <- c(mean(ship1_357780000$longitude), mean(ship1_357780000$latitude) + 5)
ship2_370016000_coor <- c(mean(ship2_370016000$longitude), mean(ship2_370016000$latitude) + 5)
ship3_219882000_coor <- c(ship3_219882000$longitude[1], mean(ship3_219882000$latitude) + 5)
ship4_372278000_coor <- c(mean(ship4_372278000$longitude), mean(ship4_372278000$latitude) + 5)

# 作图
mp + 
  geom_path(data=ship1_357780000, aes(x=longitude, y=latitude, group=group), size=1, color="red") + 
  annotate("text", x=ship1_357780000_coor[1], y=ship1_357780000_coor[2], color="red", label=357780000) + 
  geom_path(data=ship2_370016000, aes(x=longitude, y=latitude, group=group), size=1, color="orange") +
  annotate("text", x=ship2_370016000_coor[1], y=ship2_370016000_coor[2], color="orange", label=370016000) + 
  geom_path(data=ship3_219882000, aes(x=longitude, y=latitude, group=group), size=1, color="yellow") +
  annotate("text", x=ship3_219882000_coor[1], y=ship3_219882000_coor[2], color="yellow", label=219882000) + 
  geom_path(data=ship4_372278000, aes(x=longitude, y=latitude, group=group), size=1, color="green") +
  annotate("text", x=ship4_372278000_coor[1], y=ship4_372278000_coor[2], color="green", label=372278000)
