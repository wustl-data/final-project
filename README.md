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
My setup is labeled with comments, everything inside the "Gus's setup" and "End Gus's setup" is what is needed for both groups, which are lists filled with the year options and team options. There is a dictionary named team_abbr, which is used in my function so that I can use the "Schedule()" function to grab a team's entire season statistics. I have two graphs, a fourth and third down conversion rate scatterplot, with the option through a dropdown menu to select any team in the NFL and any year from 2002-2021. Both of my dcc tabs are labeled "Fourth Down Rate" and "Third Down Rate".
