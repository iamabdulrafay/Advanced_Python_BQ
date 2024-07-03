from datetime import datetime

# Write a function find_day_of_week that takes a date string in the format YYYY-MM-DD and returns the day of the week for that date.

def find_day_of_week(date_str: str) -> str:
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # - for understanding:
    # - strftime  convert date object into string and "A" is the format that give the name of the day 
    day_of_week=parsed_date.strftime("%A")
    
    print(day_of_week)
    
    
    
    

# Example Test Case1
Input= "2024-06-27"
# Output: "Thursday" 
find_day_of_week(Input)

# Example Test Case2
Input= "2024-01-01"
# Output: "Monday" 
find_day_of_week(Input)