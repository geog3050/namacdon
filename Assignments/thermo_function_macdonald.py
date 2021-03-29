def thermo():
    ''' 
    Program for inputing climate information and list of temperatures,
    then outputting determination of Folded or Unfolded. 
    Takes temperatures as list, string, or tuple; case insensitive for text inputs.
    '''

    # Gather input data
    climate_input = input("Climate Type (Tropical, Continental, etc.): ").lower()
    while True:
        try:
            input_temps = (eval(input("List of Temperatures: ")))
            if isinstance(input_temps, (str, bool, range, complex, dict, set)):
                raise SyntaxError
            elif input_temps == None:
                raise SyntaxError
        except SyntaxError:
             print("Invalid values or no temperatures entered; please try again")
        except Exception as e:
            print(e,"\n Please correct temperatures and try again")
        else:
            break
    output_type = input("Desired output format - list, string, or dictionary \
                        \n (leave blank for strings on individual lines): ").lower()
    
    # Determine threshold temperature based on climate zone
    if climate_input == 'tropical':
        climate_threshold = 30
    elif climate_input == 'continental':
        climate_threshold = 25
    else:
        climate_threshold = 18

    # Organize input temperatures into list
    temps = []
    if isinstance(input_temps, (float, int)) == True:
        temps.append(float(input_temps))
    elif isinstance(input_temps, (list,tuple)) == True:
        for item in input_temps:
            temps.append(item)    

    # Execute fold/unfold determination
    output = {}
    for t in temps:
        if t <= climate_threshold:
            output["Measurement_{}".format(len(output))] = 'F'
        else: 
            output["Measurement_{}".format(len(output))] = 'U'

    # Output data in format as requested
    if output_type == 'dictionary':
        print(output)       
    elif output_type == 'list':
        outlist = []
        for key, value in output.items():
            outlist.append(value)
        print(outlist)
    elif output_type == 'string':
        outstring = ""
        for key, value in output.items():
            outstring += value
        print(outstring)
    else:
        for key, value in output.items():
            print(value)

thermo()            
