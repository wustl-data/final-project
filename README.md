# NFL Analysis Project - CSE 314 Final Project
### Gus, Ram, Hannah, Matt
The NFL is one of the most popular sports in America, and in all sports, there is always some people that are doing things "right" and doing some things "wrong", and we wanted to find out who. We decided to analyze different aspects of the NFL, from doing statistic efficiency analysis to figuring out how much a player should make based on their statistics. We have presented our project in a Dash application, with a tab for each of the 4 members.

## Installation

To access our Dash application, clone the repo to your folder and navigate to the final-project/final_project repo. Then run the dashboard.py file.

```python
python3 final-project/final_project/dashboard.py
```
or if you navigated to the right folder
```python
python3 dashboard.py
```
## Economic Salary Model (Ram)
The inspiration for creating this model came from a debate I saw regarding two running backs on the Dallas Cowboys - Ezekiel Elliot and Tony Pollard. Elliot is a star running back and was given a massive contract, but in the past couple years, a lot of NFL fans claim that Tony Pollard is better than Elliot, especially considering how much more Elliot is being paid. People were saying that the Cowboys would regret overpaying Elliot. This made me wonder what constitutes being overpaid, and how much does a player truly deserve. I decided to create a model that would predict how much a NFL player should make based on their statistics and what the market value is (what other players are making).

The files for this model are found in this folder:
```python
final-project/final-project/final_project/ramFiles
```
I decided to create a model specifically for quarterbacks because it would be easier to start with because there  are less quarterbacks than other positions. I decided to look at only starting quarterbacks from 2021. My assumption for this model is that quarterbacks "play" themselves into a contract, which means that a player's statistics and experience is what matters in terms of contract size. For example, a player who had 4000 passing yards and 20 touchdowns should earn a greater contract than a player who had 3000 passing yards and 10 touchdowns. I also decided to not include rookie quarterbacks into the model as they technically do not have a contract based on their statistics.

#### Gathering Contract Data - spotracscrape.py

First, I prepared a list of all the starting QBs in the NFL, with the rookie quarterbacks taken out. For each quarterback, I needed to find the quarterback's current contract as well as their previous contract, and I decided to use a website called Spotrac to do so. I wrote a script called spotracscrape.py to do so. 

spotracscape.py scrapes the Spotrac website for current contract information for each Qb in a prepared list. It also scrapes data on how long the Qbs previous contract was,
information that will be used to figure out which years of statistics we need to save for each Qb. We also figure out the yearly salary for each QB here based of their contract size and years.
The data is all saved in a file called salaryData.csv.

#### Gathering Statistics - getQbStatsApi.py

Now that I have the years of each quarterback's previous contract, I needed to figure out what their statistics were during those years. I used Sports Reference to do so, and luckily they had an API available so I didn't have to scrape the website. 

getQbStatsApi.py reads in the dates from the last contract for the QBs and then uses the Sports Reference API to get the QB's statistics from these years. This data is stored in a file called qbStats.csv. 
The specific stats I decided to find for each qb were:
- completed passes
- attempted passes
- passing touchdowns
- interceptions thrown
- passing yards per attempt
- interception percentage
- quarterback rating
- yards per game played
- passing yards per attempt
- passing yards

#### Finding the right stats for the model - plots.py

I decided that I was going to create a linear model so I decided to filter out statistics that did not a linear correlation against salary. To do so, I created scatter plots with best line of fit to see how strong the correlation is between different QB stats, like years and passing yards, and salary. This was useful in figuring out which attributes are most important and should be used for the model with a visual representation. I was able to filter out statistics like interception percentage and fourth quarter comebacks, because while they were important QB statistics, they just didn't have a linear correlation. The code for my plots are on plots.py.

#### Generating Average Stats - getQBAvgStats.py and getAllAvgStats.py

Now that I knew which statistics I needed to find the average statistic per year over the length of the contract. I needed to create a function that does this to use in my model and dashboard. The following function is found in the getQBAvgStats.py file.

```Python
def getSelectedQbStats(qbName)
"""
This function gets the average statistics for a selected QB and returns this information.

* Parameters
    * qbName: string - name of the QB that stats are needed for
* Return
    * array: average statistics data for QB
"""
```

To train the model, I also needed the average statistics of all the quarterbacks in a CSV file. I prepared the script to do so in getAllAvgStats.py, in which I took the data from qbStats.csv, calculated the averages, and stored that information in a file called avgStats.csv

#### Creating the Model - lrmodel.py
Now that I had all the data I needed, it was time to create the model. Because all my data attributes seemed to have a strong linear regression, I decided to create a linear regression model, with the x value being the average statistics and the y value being the salary per year. Just to clarify, this salary per year is based on the current contract of the quarterback while the statistics are all from the previous contract of the quarterback. I used sklearn LinearRegression model to make my economic model. The following function is found inside lrmodel.py

```Python
def prepareModel()
"""
This method prepares the estimated salary linear regression model by first reading in the data from the average statistics per year CSV for each QB as well as the CSV with salary data (per year). It then uses SKlearn to prepare the model, and the first iteration of the model simply fit the model while the second iteration used a training and testing split set. 

* Parameters
    * None
* Return
    * LinearRegression: The prepared model
"""
```

#### Analyzing my model - statisticalAnalysis.py
I decided to do some analysis of my model and just quarterback salaries in general. I did some basic statistical analysis in statisticalAnalysis.py and my findings can be find in my presentation slides.

Overall, I found that my model had a strong r squared value but the root mean squared error wasn't very good. I attribute this to the fact that I only had 21 data points to built my model, and a good model needs a lot more than that.


#### Dash App
I created two ways to interact with my model in our group's dash app. The first one can be found in the "QB Economic Model (Choose from Players)" tab. I have entered every quarterback that was one of the datapoints for the model and one could choose one of the quarterbacks and see what my model says they should earn.

```Python
def update_output2(value)
"""
This method is a callback function takes the quarterback selection, finds their average statistics, generates a model, inputs the statistics into that model, and then returns the expected salary the model predicts.

* Parameters
    * value - string: name of the quarterback selected from the dropdown menu.
* Return
    * string - the expected salary predicted from the model in a string format to display on the dash app.
"""
```

I also have the "QB Economic Model (Fill in Stats)" tab where one could enter in their own custom statistics to see what a quarterback should earn based on my model.

```Python
def update_output2(value)
"""
def update_output(years, completedPasses, attemptedPasses, passingTds,ints,ydpergame,passingYards)

This method is a callback function that takes in the statistics the user wrote in the text boxes and then creates a model and inserts the statistics into the model. It then returns the model's predicted. expected salary.

* Parameters
    * years - int: the number of years
    *  completedPasses - average number of passes completed over the course of years (# of years is parameter 1)
    * attemptedPasses - average number of passes attempted over the course of years (# of years is parameter 1)
    * passingTds - average number of passing touchdowns over the course of years (# of years is parameter 1)
   * ints - average number of interceptions over the course of years (# of years is parameter 1)
   * ydpergame - average yards per game over the course of years (# of years is parameter 1)
   * passingYards - average passing yards per year over the course of years (# of years is parameter 1)

* Return
    * string - the expected salary predicted from the model in a string format to display on the dash app.
"""
```
## Third and Fourth Down Conversion Rate (Gus)
My setup is labeled with comments, everything inside the "Gus's setup" and "End Gus's setup" is what is needed for both groups, which are lists filled with the year options and team options. There is a dictionary named team_abbr, which is used in my function so that I can use the "Schedule()" function to grab a team's entire season statistics. I have two graphs, a fourth and third down conversion rate scatterplot, with the option through a dropdown menu to select any team in the NFL and any year from 2002-2021. Both of my dcc tabs are labeled "Fourth Down Rate" and "Third Down Rate". Basically how calculating the fourth and third down conversion rates are the same, so I will give an example of just fourth down: The team and year selected will go into the api, with the team being inputted into the dcitionary mentioned above, so that it converts the full team name to the abbreviated name (i.e. Chicago Bears: CHI) and then the year is obviously that team's entire season. The columns using the "Schedule" portion of the api allows me to grab the team's fourth down attempts and conversions from every game of that selected season. After putting the conversions and attempts into a variable, I would create a new variable where I put conversions divided by attempts to calculate the fourth down conversion rate for that specific game. Since conversion rate variable is a list of values, I was able to store the team's conversion rate from every game of that season into the variable.However, since the na values created an unaesthetic scatterplot, I removed all na values from the list (which mostly came from fourth down conversion, since teams attempt fourth downs less than third downs). Then created a scatterplot with the all the remaining values. For fourth down, I colored the points by if the rate was under/over 0.5 and then 0.35 for third down since teams attempt third down more often, they tend to have a lower third down conversion rate than fourth down conversion rate.
```Python
def fourth_choose_team_and_year(team,year):
    """changes graph based on team and year selected from dropdowns, initialized with the Chicago Bear's 2021 season

    Args:
        team (list of str): Selected team from dropdown
        year (list of str): Selected year from dropdown

    Returns:
        figure: Scatterplot of fourth down conversion rate for the team and year selected, na values omitted from plot
    """
```
```Python
def third_choose_team_and_year(team,year):
    """changes graph based on team and year selected from dropdowns, initialized with the Chicago Bear's 2021 season

    Args:
        team (list of str): Selected team from dropdown
        year (list of str): Selected year from dropdown

    Returns:
        figure: Scatterplot of third down conversion rate for the team and year selected, na values omitted from plot
    """
```

## College Effect: Does University of Wisconsin, which is know as RBU, prepare running backs well for the NFL?
I chose the five running backs that were active in the NFL as of last season: Jonathon Taylor, James White, Melvin Gordon, Dare Ogumbowale, and Corey Clement. They will have experienced a similar style of play and regulations in the NFL. In the past season Jonathon Taylor was very successful but I want to see if other Wisconsin running backs have seen similar success or if his success was separate from his school.
I looked at seven measures of running backs, using the sports reference api.
- Rush Attempts
- Rush Attempts per Game
- Rushing Touchdowns
- Rush Yards
- Rush Yards/Attempt
- Yards per Touch
- Times Pass Target
For each of these stats I created a helper function in hannahFiles/college.py which given an array of players fetches the stat for each and returns them in an array.
```Python
def get_yards_per_touch(players):
    """Fetches career yards per touch

    Args:
        players (array): players to retrieve career yards per touch for

    Returns:
        array: array of yards per touch for inputted players
    """
    return [player.yards_per_touch for player in players]
```
In the dashboard there is a graph for each of these measures, comparing the 5 Wisconsin Running Backs chosen.
Yards per Touch is often the most considered stat for running backs and it uses an average and so is comparable across variable lengths of careers. There are standard benchmarks for the quality of a running back based on their yards per touch, I added these benchmarks to the graph. All of the Wisconsin running backs were above the average benchmark and several were above the good. Indicating that in general Wisconsin running backs perform well in the NFL though more careful consideration of other measures is needed.
The times pass target stat is not related to rush, but helps to see if maybe a college running back is now being used more as a receiver. For example James White was low career rushing yards, but that is likely because he was more often targeted for a pass and so may have more receiving yards.

## Creating a Stat to Contextualize Pass Defense (Matt)
Using the NFL Big Data Bowl Dataset from 2021, I looked to create a statistic for pass defenses/defensive backs to better understand their performance. Within the plays.csv given, I added an extra column for the generated stat two separate times: one to look at completions and the other for incompletions. This separation is to weigh the positives and negatives of performance differently. With completions, the amount of yards on the completion is a good base to start the statistic. But with incompletions, each play is a zero yard gain which can't be used as a base differentiator. So I will go through how each the stats were made and visualized through each method. 

```Python
def get_completed_passes_df():
    """The plays file is first read in and filtered to only look at rows that are completions that gained yardage and did not result in a fumble.

    The epaYards column is then created which will be the home of the negative game impact score of a defense. The base of the stat is yards picked up on the completion. Then if the completion is greater than the yards till a first down, a multiplier between 1-1.75 is given based on what down it is to show serverity of the play in later downs. Then a 1.6 multiplier is given for plays that result in a touchdown. A final muliplier is added if the game is within 10 points and its between 1-1.3 to show serverity of the time of the game. So overall, the higher score, the worse your pass defense performed on the play. 

    The function then returns a dataframe with this added stat.
    """
    return filter_df

def get_incompleted_passes_df():
    """The plays file is first read in and filtered to only look at rows that are incompletions that did not result in a sack, penalty, fumble, intentional grounding, or unnecessary roughness.

    The epaYardsOp column is then created based on the epa column which is expected points added. The greater the expected points added the greater the incompletion as its stopping a higher chance of points added for the other team. This is multiplied by what down it is to provide severity based on the down. Similarly to the previous function we also weight if the game is close with the same multiplier. Finally we give a redzone multiplier based on how deep in the redzone the opposing team is.

    The dataframe is then returned with this additional stat. 
    """
    return filter_df
```
These are the two main functions as they create the stats we are looking at. We have two more functions to return a data frame that gives the statistical description of each of the stats based on the team with possession of the ball. I wasn't able to connect the defensive teams with all the separate plays so I decided to look at the passing offense teams throughout the season looking at both of these stats. These four function can be looked at in detail with the four different interactive graphs on my dashboard. The first graph compares yard gained on play and negatve impact with a down slection to compare how what down impacts the stat. The second looks at the negative game impact on opposing offenses. With no surprise, Kansas City's offense got the greatest average score which goes to show how good Patrick Mahomes is against defenses around the league. The third compares positive game impact to yards to end of endzone with a selection of downs. This shows where defenses were best on the field depending on the down. The last graph shows how much good defense affected offenses. Again Kansas City has the best score for an offense as their pass offense was statistically very good. 

