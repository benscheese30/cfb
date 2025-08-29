library(gt)
library(jsonlite)
library(dplyr)
library(purrr)
library(highcharter)
library(cfbfastR)

# getting team and info
team_info <- cfbd_team_info(conference = "B12")

team_names <- team_info |> 
    select(school) |> 
    pull()

# load sp+ data and combine into a single dataframe
sp_rankings <- map_dfr(1:4, function(week) {
    jsonlite::read_json(paste0("analysis/rankings/sp_plus/week_", week, ".json")) |> 
        map_dfr(~ unlist(.)) |> 
        mutate(
            week = week,
            rating = as.numeric(rating),
            ranking = as.integer(ranking),             
            offense.ranking = as.numeric(offense.ranking),
            offense.rating = as.integer(offense.rating),     
            defense.ranking = as.numeric(defense.ranking),
            defense.rating = as.integer(defense.rating),      
            specialTeams.rating = as.numeric(specialTeams.rating)
        )
})  

fpi_rankings <- purrr::map_dfr(1:4, function(week) {
    jsonlite::read_json(paste0("analysis/rankings/fpi/week_", week, ".json")) |> 
        map_dfr(~ unlist(.)) |> 
        mutate(
            week = week,
            year = as.integer(year),
            fpi = as.numeric(fpi),
            resumeRanks.strengthOfRecord = as.integer(resumeRanks.strengthOfRecord),
            resumeRanks.fpi = as.integer(resumeRanks.fpi),
            resumeRanks.averageWinProbability = as.integer(resumeRanks.averageWinProbability),
            resumeRanks.strengthOfSchedule = as.integer(resumeRanks.strengthOfSchedule),
            resumeRanks.remainingStrengthOfSchedule = as.integer(resumeRanks.remainingStrengthOfSchedule),
            resumeRanks.gameControl = as.integer(resumeRanks.gameControl)
        )
}) |> 
    mutate(
        efficiencies.overall = as.numeric(efficiencies.overall),
        efficiencies.offense = as.numeric(efficiencies.offense),
        efficiencies.defense = as.numeric(efficiencies.defense),
        efficiencies.specialTeams = as.numeric(efficiencies.specialTeams)
    )


# preparing sp+ dataframe for highcharts
sp_ranking_chart <- data.frame()

# we are creating a week for each team and then joining the current rankings into it
for (t in team_names){
    sp_ranking_chart <- rbind(
        sp_ranking_chart,
        data.frame(
            week = c(1:14),
            team = t
        )
    )
}

sp_ranking_chart <- sp_ranking_chart |> 
    left_join(
        sp_rankings |> 
            filter(
                conference == 'Big 12'
            ),
        by = c("week", "team")
    ) |> 
    left_join(
        team_info |> 
            rename(
                team = school
            ) |> 
            select(
                team, 
                color,
                alt_color,
                logo,
                logo_2
            ),
        by = "team"
    ) |> 
    group_by(
        week
    ) |> 
    mutate(
        normalized_ranking = ifelse(is.na(year), NA, rank(ranking, ties.method = "first"))
    ) |> 
    ungroup()

highchart() |> 
    hc_add_series_list(
        sp_ranking_chart |> 
            group_by(
                name = team,
                color = ifelse(is.na(color), alt_color, color)
            ) |> 
            do(
                data = list_parse(
                    data.frame(name = .$week, y = .$normalized_ranking, logo_png = .$logo)
                )
            )
    ) |> 
    hc_title(
        text = "Big 12 Sp+ Rankings by Week"
    ) |> 
    hc_yAxis(
        title = list(
            text = "Rank"
        ),
        opposite = FALSE,
        reversed = TRUE,
        tickInterval = 1,
        showFirstLabel = FALSE,
        showLastLabel = FALSE
    ) |> 
    hc_xAxis(
        title = list(
            text = "Week"
        ),
        type = "category"
    ) |> 
    hc_plotOptions(
        series = list(
            dataLabels = list(
                enabled = TRUE,
                useHTML = TRUE,
                align = "left",  # Align the label to the left of the point
                verticalAlign = "middle",
                formatter = JS("function() {
                    if (this.point.index === 3) {  // Check if the point is the second one (index 1)
                        var logo = this.point.logo_png;
                        return '<img src=\"' + logo + '\" style=\"width:28px;height:28px;\"/>';
                    } else {
                        return null;  // No label for other points
                    }
                }")
            ),
            marker = list(
                symbol = "circle",
                radius = 2.5
            )
        )
    ) |> 
    hc_legend(
        enabled = FALSE
    )


# preparing fpi dataframe for highcharts
fpi_ranking_chart <- data.frame()

# we are creating a week for each team and then joining the current rankings into it
for (t in team_names){
    fpi_ranking_chart <- rbind(
        fpi_ranking_chart,
        data.frame(
            week = c(1:14),
            team = t
        )
    )
}

fpi_ranking_chart <- fpi_ranking_chart |> 
    left_join(
        fpi_rankings |> 
            filter(
                conference == 'Big 12'
            ) |> 
            select(
                year,
                week,
                team,
                rank = resumeRanks.fpi
            ),
        by = c('week', 'team')
    ) |> 
    left_join(
        team_info |>
            select(
                team = school, 
                color,
                alt_color,
                logo,
                logo_2
            ),
        by = "team"
    ) |> 
    group_by(
        week
    ) |> 
    mutate(
        normalized_ranking = ifelse(is.na(year), NA, rank(rank, ties.method = "first"))
    ) |> 
    ungroup()

highchart() |> 
    hc_add_series_list(
        fpi_ranking_chart |> 
            group_by(
                name = team,
                color = ifelse(is.na(color), alt_color, color)
            ) |> 
            do(
                data = list_parse(
                    data.frame(name = .$week, y = .$normalized_ranking, logo_png = .$logo)
                )
            )
    ) |> 
    hc_title(
        text = "Big 12 FPI Rankings by Week"
    ) |> 
    hc_yAxis(
        title = list(
            text = "Rank"
        ),
        opposite = FALSE,
        reversed = TRUE,
        tickInterval = 1,
        showFirstLabel = FALSE,
        showLastLabel = FALSE
    ) |> 
    hc_xAxis(
        title = list(
            text = "Week"
        ),
        type = "category"
    ) |> 
    hc_plotOptions(
        series = list(
            dataLabels = list(
                enabled = TRUE,
                useHTML = TRUE,
                align = "left",  # Align the label to the left of the point
                verticalAlign = "middle",
                formatter = JS("function() {
                    if (this.point.index === 3) {  // Check if the point is the second one (index 1)
                        var logo = this.point.logo_png;
                        return '<img src=\"' + logo + '\" style=\"width:24px;height:24px;\"/>';
                    } else {
                        return null;  // No label for other points
                    }
                }")
            ),
            marker = list(
                symbol = "circle",
                radius = 3
            )
        )
    ) |> 
    hc_legend(
        enabled = FALSE
    )
