# NFL Analysis Project - CSE 314 Final Project
## Gus, Ram, Hannah, Matt
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

## Third and Fourth Down Conversion Rate (Gus)
My setup is labeled with comments, everything inside the "Gus's setup" and "End Gus's setup" is what is needed for both groups, which are lists filled with the year options and team options. There is a dictionary named team_abbr, which is used in my function so that I can use the "Schedule()" function to grab a team's entire season statistics. I have two graphs, a fourth and third down conversion rate scatterplot, with the option through a dropdown menu to select any team in the NFL and any year from 2002-2021. Both of my dcc tabs are labeled "Fourth Down Rate" and "Third Down Rate".
