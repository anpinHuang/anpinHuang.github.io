library(sqldf)
library(reshape)
library(igraph)
raw_fights <- read.csv("/Users/smartboyben/Documents/git/anpinHuang.github.io/UFC/data.csv")
## if there is a rematch, take the average

fights_sort <- sqldf("select case when R_fighter < B_fighter then R_fighter else B_fighter end as f1
                      , case when R_fighter > B_fighter then R_fighter else B_fighter end as f2
                      , case when (R_fighter < B_fighter and Winner = 'Red') or (R_fighter > B_fighter and Winner = 'Blue')  then 1 else 0 end f1_win
                     from raw_fights
                     order by f1 asc")
R_fights_count <- sqldf("select R_fighter fighter, count() no_fights from raw_fights r1 where date > '2010-01-01' group by 1 order by no_fights desc")
B_fights_count <- sqldf("select B_fighter fighter, count() no_fights from raw_fights r1 where date > '2010-01-01' group by 1 order by no_fights desc")
fights_count_raw <- sqldf('select * from R_fights_count union select * from B_fights_count')
fights_count <- sqldf('select fighter, sum(no_fights) no_fights from fights_count_raw group by 1 order by no_fights desc')

## only consider fighters with more than 5 (6 up) fights
full_time <- fights_count[which(fights_count$no_fights>5),]
fights_sort <- fights_sort[which(fights_sort$f1 %in% full_time$fighter & fights_sort$f2 %in% full_time$fighter ),]


fights_sort_avg <- sqldf("select f1, f2, avg(f1_win+0.0) over (partition by f1||f2) as f1_win_a, row_number() over (partition by f1||f2) rowN from fights_sort")

fights_sort_avg <- sqldf("select f1, f2, f1_win_a from fights_sort_avg where rowN = 1")
## check Conor McGregor
fights_sort[which(fights_sort$f1=='Conor McGregor' | fights_sort$f2=='Conor McGregor'),]
fights_sort_avg[which(fights_sort_avg$f1=='Conor McGregor' | fights_sort_avg$f2=='Conor McGregor'),]

to_wide <- reshape(data = fights_sort_avg, idvar = 'f1', timevar = 'f2', direction = 'wide')
row.names(to_wide) <- to_wide[,1]
to_wide <- to_wide[,-1]

min_date <- sqldf("select min(date) from raw_fights")

relations <- sqldf("select case when winner = 'Red' then B_fighter else R_fighter end as _from 
                    ,case when winner = 'Red' then R_fighter else B_fighter end as _to
                    from raw_fights
                    where weight_class = 'Lightweight'")
colnames(relations) <- c('from','to')
g <- graph_from_data_frame(relations, directed=TRUE)
rank <- page.rank(g)
rank$vector <- rank$vector[order(rank$vector, decreasing = T)]
top <- as.data.frame(head(rank$vector,20))
top$fighter <- rownames(top)

raw_fights_top <- sqldf("select r.* 
                        from raw_fights r 
                        where r.R_fighter in (select top.fighter from top) 
                        and r.B_fighter in (select top.fighter from top)")

relations_top <- sqldf("select case when winner = 'Red' then B_fighter else R_fighter end as _from 
                    ,case when winner = 'Red' then R_fighter else B_fighter end as _to
                    from raw_fights_top
                    where weight_class = 'Lightweight'")

colnames(relations_top) <- c('from','to')
g_top <- graph_from_data_frame(relations_top, directed=TRUE)
rank_top <- page.rank(g_top)
rank_top$vector <- rank_top$vector[order(rank_top$vector, decreasing = T)]
as.data.frame(head(rank_top$vector,20))
#top$fighter <- rownames(top)

MJ <- sqldf("select r.* 
            from raw_fights_top r 
            where B_fighter = 'Michael Johnson' or R_fighter = 'Michael Johnson'
            and weight_class = 'Featherweight'")
MJ[,1:8]

KN <- sqldf("select r.* 
            from raw_fights_top r 
            where B_fighter = 'Khabib Nurmagomedov' or R_fighter = 'Khabib Nurmagomedov'
            ")
KN[,1:8]
