library(shiny)
library(httr)
library(jsonlite)
library(ggplot2)

# Define UI
ui <- fluidPage(
  titlePanel("User Analytics Dashboard"),
  
  sidebarLayout(
    sidebarPanel(
      h3("Controls"),
      actionButton("refresh", "Refresh Data", class = "btn-primary"),
      hr(),
      textOutput("user_count")
    ),
    
    mainPanel(
      h3("User Age Distribution"),
      plotOutput("age_pie_chart", height = "400px"),
      hr(),
      h4("User Data"),
      tableOutput("user_table")
    )
  )
)

# Define server logic
server <- function(input, output, session) {
  
  # Reactive value to store users data
  users_data <- reactiveVal(NULL)
  
  # Fetch users from FastAPI
  fetch_users <- function() {
    tryCatch({
      response <- GET("http://localhost:8000/users")
      
      if (status_code(response) == 200) {
        users <- fromJSON(content(response, "text", encoding = "UTF-8"))
        return(users)
      } else {
        return(NULL)
      }
    }, error = function(e) {
      return(NULL)
    })
  }
  
  # Fetch data on app start
  observe({
    users_data(fetch_users())
  })
  
  # Refresh data when button is clicked
  observeEvent(input$refresh, {
    users_data(fetch_users())
  })
  
  # Display user count
  output$user_count <- renderText({
    users <- users_data()
    if (is.null(users) || nrow(users) == 0) {
      "No users found"
    } else {
      paste("Total Users:", nrow(users))
    }
  })
  
  # Create pie chart of user ages
  output$age_pie_chart <- renderPlot({
    users <- users_data()
    
    if (is.null(users) || nrow(users) == 0) {
      plot.new()
      text(0.5, 0.5, "No data available\nClick 'Refresh Data' or add users via API", cex = 1.5)
    } else {
      # Create age groups
      users$age_group <- cut(users$age, 
                             breaks = c(0, 20, 30, 40, 50, 100),
                             labels = c("0-20", "21-30", "31-40", "41-50", "50+"),
                             right = TRUE)
      
      # Count users in each age group
      age_counts <- as.data.frame(table(users$age_group))
      colnames(age_counts) <- c("Age_Group", "Count")
      
      # Create pie chart
      ggplot(age_counts, aes(x = "", y = Count, fill = Age_Group)) +
        geom_bar(stat = "identity", width = 1, color = "white") +
        coord_polar("y", start = 0) +
        theme_void() +
        labs(fill = "Age Group") +
        geom_text(aes(label = Count), position = position_stack(vjust = 0.5), size = 6) +
        scale_fill_brewer(palette = "Set3")
    }
  })
  
  # Display user table
  output$user_table <- renderTable({
    users <- users_data()
    
    if (!is.null(users) && nrow(users) > 0) {
      users[, c("id", "name", "age", "address")]
    }
  })
}

# Run the application
shinyApp(ui = ui, server = server)

