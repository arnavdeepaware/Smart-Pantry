def find_calories(is_female, current_weight, target_weight, current_height, age, time_period):
    """
    Calculate daily calorie intake based on current weight, target weight, height, age, and time period.
    
    :param is_female: Boolean indicating gender (True for female, False for male)
    :param current_weight: Current weight in kg
    :param target_weight: Target weight in kg
    :param current_height: Height in cm
    :param age: Age in years
    :param time_period: Time period in weeks to reach target weight
    :param activity_level: Activity level factor (1.2 - sedentary, 1.375 - lightly active, 
                           1.55 - moderately active, 1.725 - active, 1.9 - very active)
    :return: Daily calorie intake needed to achieve the goal within the given time
    """
    if time_period <= 0:
        raise ValueError("Time period must be greater than zero.")
    
    # Calculate BMR
    if is_female:
        bmr = 655.1 + (9.563 * current_weight) + (1.850 * current_height) - (4.676 * age)
    else:
        bmr = 66.47 + (13.75 * current_weight) + (5.003 * current_height) - (6.755 * age)
    
    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = bmr * 1.55  # Moderately active
    
    # Calculate calorie adjustment per day
    weight_change = current_weight - target_weight  # Positive for weight loss, negative for gain
    calorie_adjustment = (weight_change / time_period) * 500
    
    # Target daily calorie intake with minimum safety threshold
    target_calories = max(1500, tdee - calorie_adjustment)
    
    return round(target_calories, 2)

def test_calculator():
    # Test Case 1: Male weight loss (1 month)
    result1 = find_calories(False, 75.0, 72.0, 175.0, 25, 1)
    print(f"Test 1 (Male weight loss - 1 month): {result1} calories/day")

    # Test Case 2: Female weight loss (3 months)
    result2 = find_calories(True, 65.0, 60.0, 165.0, 30, 3)
    print(f"Test 2 (Female weight loss - 3 months): {result2} calories/day")

    # Test Case 3: Maintenance (6 months)
    result3 = find_calories(False, 70.0, 70.0, 170.0, 28, 6)
    print(f"Test 3 (Maintenance - 6 months): {result3} calories/day")

    # Test Case 4: Male weight loss (12 months)
    result4 = find_calories(False, 80.0, 70.0, 180.0, 35, 12)
    print(f"Test 4 (Male weight loss - 12 months): {result4} calories/day")

if __name__ == "__main__":
    test_calculator()