import random
# Game variables
game_vars = {
    'day': 1,
    'energy': 10,
    'money': 200,
    'bag': {},
}

seed_list = ['LET', 'POT', 'CAU']
seeds = {
    'LET': {'name': 'Lettuce',
            'price': 2,
            'growth_time': 2,
            'crop_price': 3
            },

    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6
            },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14
            },
}

invalid_message = ["OOPS! That's not a valid option. Try again!", "Nice try but thats not an option, choose again!", \
                   "Nope try again, even the cows are laughing.", "Are you farming or just guessing? Choose an available option!", \
                    "ERROR 404, Choice not found. Try again!", "Wrong choice! The crops aren't going to plant themselves so hurry up!"]
invalid_string = ["OOPS! Did your keyboard slip? Only numbers pls!", "Should I feed the letters to the cows? Input an integer pls!", \
                  "Please try again, the potatos won't grow if you continue to input strings"]

farm = [ ['----', '----', '----', '----', '----'],
         ['----', '----', '----', '----', '----'],
         ['----', '----', 'House', '----', '----'],
         ['----', '----', '----', '----', '----'],
         ['----', '----', '----', '----', '----'] ]

farmer_row, farmer_col = 2, 2
on_seed = False
can_harvest = False
#-----------------------------------------------------------------------
# in_town(game_vars)
#
#    Shows the menu of Albatross Town and returns the player's choice
#    Players can
#      1) Visit the shop to buy seeds
#      2) Visit the farm to plant seeds and harvest crops
#      3) End the day, resetting Energy to 10 and allowing crops to grow
#
#      9) Save the game to file
#      0) Exit the game (without saving)
#-----------------------------------------------------------------------

def in_town(game_vars):
    while True:
        show_stats(game_vars)
        print("""You are in Albatross Town
-------------------------
1) Visit Shop
2) Visit Farm
3) End Day

9) Save Game
0) Exit Game
-------------------------""")
        try:
            town_choice = int(input("Your Choice? ")) 
        except:
            #if user input is not an integer, prints error message and continues loop
            print(invalid_message[random.randint(0,5)])
            continue
        else:
            #if user input is not an option, prints error message and continues loop
            if town_choice not in [1,2,3,9,0]:
                print(invalid_message[random.randint(0,5)])
                continue
            else:
                return town_choice
            
#----------------------------------------------------------------------
# in_shop(game_vars)
#
#    Shows the menu of the seed shop, and allows players to buy seeds
#    Seeds can be bought if player has enough money
#    Ends when player selects to leave the shop
#----------------------------------------------------------------------


def in_shop(game_vars):
    while True:
        print("Welcome to Pierce's Seed Shop!")
        show_stats(game_vars)

        #prints shop headers)
        print(f"""What do you wish to buy?
{'Seed':<16} {'Price':^5}  {'Days to Grow':^15} {'Crop Price':^10}
--------------------------------------------------""")
        
        #prints seed details by getting details from seeds dictionary
        for i in range(len(seed_list)):
            seed_code = seed_list[i]
            seed_info = seeds[seed_code]
            print(f" {i+1}) {seed_info['name']:<12} {seed_info['price']:^5} {seed_info['growth_time']:^15}  {seed_info['crop_price']:^10}")
        print('\n 0) Leave\n--------------------------------------------------')
        
        #Finds total amount of seeds currently in bag
        total_seeds = 0
        for seed in game_vars['bag']:
            total_seeds += game_vars['bag'][seed]
        if total_seeds == 10:
            print('Your bag contains 10 seeds! You cannot buy anymore! ')


        try:
            shop_choice = int(input("Your choice? "))
            #ensures that shop choice is a non negative integer 
            assert shop_choice >= 0
            #stops function by returning, when user wants to leave
            if shop_choice == 0:
                return
            
            #If bag already has 10 seeds, user can only leave the shop
            elif total_seeds == 10:
                print(invalid_message[random.randint(0,5)])
                continue
            
            seed_name = seed_list[shop_choice - 1] #gets seed name from seed list
            #checks if user has enough money to buy at least 1 seed, else continues loop
            if game_vars['money'] >= seeds[seed_name]['price']: 
                print(f"You have ${game_vars['money']}")
                buy_amount = int(input("How many do you wish to buy? "))
                #If total seeds to buy would exceed 10, purchase is rejected
                if buy_amount + total_seeds > 10:
                    print(f"Looks like your bag is not big enough!\nBag Space: {total_seeds}/10")
                    continue
                #ensures amount of seeds to purcahse is non negative
                assert buy_amount >= 0
                #checks if user has enough money to buy the amount of seeds inputed
                if buy_amount * seeds[seed_name]['price'] <= game_vars['money']:
                    game_vars['money'] -= buy_amount * seeds[seed_name]['price']
                    if seed_name in game_vars['bag']:
                        game_vars['bag'][seed_name] += buy_amount
                    else:
                        game_vars['bag'][seed_name] = buy_amount

                    print(f"You bought {buy_amount} {seeds[seed_name]['name']} seeds.")
                else:
                    print("You can't afford that!")
                    continue
            else:
                print("You can't afford that!")

        except:
            print(invalid_string[random.randint(0,2)])
            continue
        
#----------------------------------------------------------------------
# draw_farm(farm, farmer_row, farmer_col)
#
#    Draws the farm
#    Each space on the farm has 3 rows:
#      TOP ROW:
#        - If a seed is planted there, shows the crop's abbreviation
#        - If it is the house at (2,2), shows 'HSE'
#        - Blank otherwise
#      MIDDLE ROW:
#        - If the player is there, shows X
#        - Blank otherwise
#      BOTTOM ROW:
#        - If a seed is planted there, shows the number of turns before
#          it can be harvested
#        - Blank otherwise
#----------------------------------------------------------------------

def draw_farm(farm, farmer_row, farmer_col):
    for row in range(len(farm)):
        print("+-----" * len(farm) + "+")
        for i in range(3): #loops for 3 rows in the farm for each row in the farm nestled loop
            for col in range(len(farm[row])):
                if i == 0: #first loop of the row
                    if farm[row][col] == 'House':
                        print(f"| HSE ", end = '')
                    elif farm[row][col] == '----':
                        print("|     ", end = '')
                    else:
                        #prints any seeds for each row in farm if there is
                        print(f"| {farm[row][col][:3]} ", end = '')

                elif i == 1: #second loop of the row
                    #prints farmer if it matches with the row and column of farmer, otherwise blank space
                    if row == farmer_row and col == farmer_col:
                        print("|  X  ", end = '')
                    else:
                        print("|     ", end = '')
                else: #last loop of the row
                    if farm[row][col] not in ['----', 'House']:
                        print(f"|  {farm[row][col][-1]}  ", end = '')
                    else:
                        print("|     ", end = '')
            print('|') #closes the farm at the end of every row
    print("+-----" * len(farm) + "+") #prints line to close the farm


#----------------------------------------------------------------------
# in_farm(game_vars, farm))
#
#    Handles the actions on the farm. Player starts at (2,2), at the
#      farmhouse.
#
#    Possible actions:
#    W, A, S, D - Moves the player
#      - Will show error message if attempting to move off the edge
#      - If move is successful, Energy is reduced by 1
#
#    P - Plant a crop
#      - Option will only appear if on an empty space
#      - Shows error message if there are no seeds in the bag
#      - If successful, Energy is reduced by 1
#
#    H - Harvests a crop
#      - Option will only appear if crop can be harvested, i.e., turns
#        left to grow is 0
#      - Option shows the money gained after harvesting
#      - If successful, Energy is reduced by 1
#
#    R - Return to town
#      - Does not cost energy
#----------------------------------------------------------------------
def in_farm(game_vars, farm, farmer_row, farmer_col):
    while True:
        #checks if any seeds in bag has quantity of zero, if there is, removes seed. Loop is not needed, only 1 seed at 0 at any time.
        seed_to_remove = ''
        for seed in game_vars['bag']:
            if game_vars['bag'][seed] == 0:
                seed_to_remove = seed
        if seed_to_remove != '':
            game_vars['bag'].pop(seed_to_remove)

        draw_farm(farm, farmer_row, farmer_col)

        print(f"Energy: {game_vars['energy']}\n[WASD] Move\n[R]eturn to Town")

        #checks if the last character of the cell the user is standing on is a number (means that there is a seed there), or if farmer is standing on house. If true, sets can plant to false. Else, sets can plant to true and can harvest to false
        if farm[farmer_row][farmer_col][-1].isdigit() or farm[farmer_row][farmer_col] == 'House':
            can_plant = False
            #checks if the last character of the cell the user is standing on is 0 (means that crop can be harvested). If true, sets can harvest to true
            if farm[farmer_row][farmer_col][-1] == '0':
                can_harvest = True
                print(f"[H]arvest {seeds[farm[farmer_row][farmer_col][:3]]['name']} for ${seeds[farm[farmer_row][farmer_col][:3]]['crop_price']}")
            else:
                can_harvest = False
        else:
            can_plant = True
            can_harvest = False
            print('[P]lant seed')
        
        action_choice = input("Your choice? ")
        if action_choice.isalpha() and len(action_choice) == 1:
            action_choice = action_choice.upper()
        else:
            print("Please only input a 1 character letter")
            continue

        try:
            #ensures actions can only be done if energy is more than 0
            if game_vars['energy'] > 0:
                if action_choice == 'W':
                    if farmer_row == 0:
                        print('There are trees in front of you!')
                    else:
                        farmer_row -= 1
                        game_vars['energy'] -= 1

                elif action_choice == 'A':
                    if farmer_col == 0:
                        print('There a boulder to your left!')
                    else:
                        farmer_col -= 1
                        game_vars['energy'] -= 1
                    
                elif action_choice == 'S':
                    if farmer_row == 4:
                        print('Theres a family of birds behind you!')
                    else:
                        farmer_row += 1
                        game_vars['energy'] -= 1

                elif action_choice == 'D':
                    if farmer_col == 4:
                        print('There is a cliff to your right!')
                    else:
                        farmer_col += 1
                        game_vars['energy'] -= 1

                elif action_choice == 'R':
                    farmer_row, farmer_col = 2, 2
                    break

                elif can_plant:
                    if action_choice == 'P':
                        print(f"""What do you wish to plant?
------------------------------------------------------------------
{'Seed':^15} {'Days to Grow':>17} {'Crop Price':>15} {'Available':>15}
------------------------------------------------------------------""")
                        plant_seed_counter = 1 #to print each option of the seeds to plant in bag
                        availble_seed_list = [] #appends available seeds into list
                        #fetches data from seeds dictionary to print it out, and quantity from bag. Appends seed in the bag into list for indexing later 
                        for seed in game_vars['bag']:
                            print(f" {plant_seed_counter}) {seeds[seed]['name']:<21} {seeds[seed]['growth_time']:<16} {seeds[seed]['crop_price']:<16} {game_vars['bag'][seed]:<15} ")
                            plant_seed_counter += 1
                            availble_seed_list.append(seed)
                        print("\n 0)  Leave\n")
                        #continues process of item buying by indexing choice from the list created
                        plant_seed_choice = int(input("Your Choice? ")) - 1
                        farm[farmer_row][farmer_col] = availble_seed_list[plant_seed_choice] + str(seeds[availble_seed_list[plant_seed_choice]]['growth_time'])
                        game_vars['bag'][farm[farmer_row][farmer_col][:3]] -= 1
                        game_vars['energy'] -= 1

                elif can_harvest:
                    if action_choice == 'H':
                        #Adds crop price to money, and fills back farm space to empty
                        game_vars['money'] += seeds[farm[farmer_row][farmer_col][:3]]['crop_price']
                        print(f"You harvested the {seeds[farm[farmer_row][farmer_col][:3]]['name']} and sold it for ${seeds[farm[farmer_row][farmer_col][:3]]['crop_price']}!")
                        print(f"You now have ${game_vars['money']}!")
                        farm[farmer_row][farmer_col] = '----'
                        game_vars['energy'] -= 1

                
                else:
                    print(invalid_message[random.randint(0,5)])

            else:
                if action_choice == 'R':
                    farmer_row, farmer_col = 2, 2
                    break
                print("You're too tired. You should get back to town.")

        except:
            print(invalid_string[random.randint(0,2)])
            continue

#----------------------------------------------------------------------
# show_stats(game_vars)
#
#    Displays the following statistics:
#      - Day
#      - Energy
#      - Money
#      - Contents of Seed Bag
#----------------------------------------------------------------------
def show_stats(game_vars):
    #prints stats formatted inside boxes
    print(f"""+--------------------------------------------------+
| Day {game_vars['day']:<11} Energy: {game_vars['energy']:<10} Money: ${game_vars['money']:<5} |
| {'Your seeds:':<48} |""")
    if game_vars['bag']:
        for i in game_vars['bag']:
            print(f"| {seeds[i]['name']:>12}: {game_vars['bag'][i]:<9} {'|':>26}")
    else:
        print(f'{"| You have no seeds":<50} |')
    print('+--------------------------------------------------+')

#----------------------------------------------------------------------
# end_day(game_vars)
#
#    Ends the day
#      - The day number increases by 1
#      - Energy is reset to 10
#      - Every planted crop has their growth time reduced by 1, to a
#        minimum of 0
#----------------------------------------------------------------------
def end_day(game_vars):
    print()
    variable_crop_prices(seeds, seed_list)
    #Code occurs when game is won, then stops game
    if game_vars['money'] >= 100:
        print(f"""You have ${game_vars['money']} after {game_vars['day']} days.
You paid off your debt of $100 and made a profit of ${game_vars['money'] - 100}!
You Win!""")
        exit()
    #Code occurs when game is lost, then stops game
    elif game_vars['day'] >= 20:
        print("You have reached day 20 without making $100, try again after learning how to plant crops better!\nYou Lost!")
        exit()
    #Else, continues game as usual
    game_vars['day'] += 1
    game_vars['energy'] = 10
    for row in range(len(farm)):
        for col in range(len(farm[0])):
            if farm[row][col][-1].isdigit() and farm[row][col][-1] != '0':    
                farm[row][col] = farm[row][col][:3] + str(int(farm[row][col][-1]) - 1)

def variable_crop_prices(seeds, seed_list):
    for i in range(len(seed_list)):
        seed_name = seed_list[i]
        #Gets upper and lower limit for seed price, so that price goes up or down by either $1 or $2
        upperlimit = seeds[seed_name]['crop_price'] + random.randint(1,2)
        lowerlimit = seeds[seed_name]['crop_price'] - random.randint(1,2)
        #Holds the previous price of seed to compare it with the current one
        normal_price = seeds[seed_name]['crop_price']
        #Defines new crop price
        seeds[seed_name]['crop_price'] = random.randint(lowerlimit, upperlimit)
        #Prints popularity of the crop to update user of increase/decrease of prices
        if normal_price == seeds[seed_name]['crop_price']:
            print(f"Looks like the price of {seeds[seed_name]['name']} is normal today!")
        elif normal_price > seeds[seed_name]['crop_price']:
            print(f"Looks like {seeds[seed_name]['name']} is not popular today!")
        else:
            print(f"Looks like {seeds[seed_name]['name']} is popular today!")



#----------------------------------------------------------------------
# save_game(game_vars, farm)
#
#    Saves the game into the file "savegame.txt"
#----------------------------------------------------------------------
def save_game(game_vars, farm):
    #Create WorldList if it does not exist
    try:
        with open('WorldList.txt', 'r') as testfile:
            pass
    except FileNotFoundError:
        with open('WorldList.txt', 'w') as create_file:
            print('Text file "WorldList" has been created to store world data.')
        
    while True:
        world_count = 0 #counts the number of worlds
        world_list = [] #to store the name of all worlds
        #WorldList is a text file that stores all world names
        #Below code prints all worlds that have been saved
        with open('WorldList.txt', 'r') as worlds:
            print("Saved Worlds:\n-----------------------------")
            for line in worlds:
                line = line.strip()
                print(f"{world_count + 1}) {line}")
                world_list.append(line)
                world_count += 1
            print("\n0) New World\n-----------------------------")
            try:
                world_save = int(input("Which world do you want to save this as? "))
                if world_save < 0 or world_save > world_count:
                    raise ValueError #Raises error to continue while loop if world save is not a valid option
            except:
                print(invalid_message[random.randint(0,5)])
                continue

            if world_save == 0:
                file = input("What do you want to call this world? ")
                world_list.append(file) 
                with open('WorldList.txt', 'a') as worlds:
                    worlds.write(file + '\n')
            else:
                #Defines file as the file which we want to save the world in
                file = world_list[world_save - 1]
            break
        
    with open(file + '.txt', "w") as SaveFile:
        for row in farm:
            temp_string = '' #Temp string is to temp hold data of each row of the farm in a string
            for cell in row:
                temp_string += '|' + cell
            temp_string = temp_string[1:] #gets rid of first "|" before writing it to SaveFile
            SaveFile.write(temp_string + '\n')
            
           #Saves all game variables which are not the bag 
        for value in game_vars:
            if value != 'bag':
                SaveFile.write(value + '|' + str(game_vars[value]) + '\n')

        #saves items in bag as a string, similar to the way farm is saved
        item_to_write = ''
        for item in game_vars['bag']:
            item_to_write += '|' + item + ',' + str(game_vars['bag'][item])
        item_to_write = item_to_write[1:]
        SaveFile.write(item_to_write)
    print(f"Game data has been successfully into {file}")



#----------------------------------------------------------------------
# load_game(game_vars, farm)
#
#    Loads the saved game by reading the file "savegame.txt"
#----------------------------------------------------------------------
def load_game(game_vars, farm):
    #Create WorldList if it does not exist
    try:
        with open('WorldList.txt', 'r') as testfile:
            pass
    except FileNotFoundError:
        with open('WorldList.txt', 'w') as create_file:
            print('Text file "WorldList" has been created to store world data.')


    while True:
        #Following code is similar to the one in save_game
        #Below code prints all worlds that have been saved
        world_count = 0
        world_list = []

        with open('WorldList.txt', 'r') as worlds:
            print("Saved Worlds:\n-----------------------------")
            for line in worlds:
                line = line.strip()
                print(f"{world_count + 1}) {line}")
                world_list.append(line)
                world_count += 1
            print("-----------------------------")
            try:
                world_save = int(input("Which world do you want to load? "))
                if world_save <= 0 or world_save > world_count:
                    raise ValueError #Raises error to continue while loop if world to load is not valid
            except:
                print(invalid_message[random.randint(0,5)])
                continue
            file = world_list[world_save - 1] #defines the file we want to load
            break
            
    print(f"World [{file}] has been successfully loaded")    

    with open(file + ".txt", 'r') as LoadFile:
        count = 0
        for line in LoadFile:
            #removes "\n" at the back of any line if it exists
            if line[-1] == '\n':
                line = line[:-1]
            line = line.split('|') #splits by "|" to create a list, so that data can be seperated
            if len(line) == 5: #checks for data values which is a farm, since only farm is always length of 5
                farm[count] = line

            elif len(line) == 2 and line[0] in ['day', 'energy', 'money']:
                game_vars[line[0]] = int(line[1])

            else:
                #splits data saved in text file for seeds, and saves it to game variables
                for plant in line:
                    plant = plant.split(',')
                    game_vars['bag'][plant[0]] = int(plant[1])

            count += 1

#----------------------------------------------------------------------
#    Main Game Loop
#----------------------------------------------------------------------


while True:
    print("----------------------------------------------------------")
    print("Welcome to Sundrop Farm!")
    print()
    print("You took out a loan to buy a small farm in Albatross Town.")
    print("You have 20 days to pay off your debt of $100.")
    print("You might even be able to make a little profit.")
    print("How successful will you be?")
    print("----------------------------------------------------------")
    print("""1) Start a new game
2) Load your saved game
0) Exit Game""")
    try:
        menu_choice = int(input("Your Choice? "))
    except:
        print(invalid_message[random.randint(0,5)])
        continue
    else:
        #Quits game if menu choice is 0
        if menu_choice == 0:
            exit()
        elif menu_choice == 1:
            break
        elif menu_choice == 2:
            load_game(game_vars, farm)
            break
        else:
            print(invalid_message[random.randint(0,5)])



# Write your main game loop here
#in_town(game_vars)
#in_shop(game_vars)
#in_farm(game_vars, farm, farmer_row, farmer_col)

while True:
    in_town_choice = in_town(game_vars)
    if in_town_choice == 1:
        in_shop(game_vars)
    elif in_town_choice == 2:
        in_farm(game_vars, farm, farmer_row, farmer_col)
    elif in_town_choice == 3:
        end_day(game_vars)
    elif in_town_choice == 9:
        save_game(game_vars, farm)
    else:
        break

