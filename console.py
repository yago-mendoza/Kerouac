######################################################################

# *** DISCLAIMER ***
# This python script is provisional until a more complex interface
# appropriate to Kerouac's objective is developed. It allows only
# the insertion of data, not its query, as well as the hinting method.
# However, its coding is rather lax in terms of adequacy. A mess.

# Compiling :

# pyinstaller --console --icon=icon.ico --add-data "Kerouac.txt;." console.py

######################################################################

from components import Database
import datetime
import random
import utils
import os

get_time = lambda : datetime.datetime.now().strftime('%H.%M.%S')

def clear_screen ():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

Database.build()
clear_screen()

FINISH = False
SUGG_MODE = False
FIELD = None
PS1 = get_time()+'[]@[] >> '
EDITED = False
BATCH = []
NCOL = 3
N_CHANGES_YET = 0
DETAILS_FEATURE = True
AUTOSAVE_FEATURE = True
NEW_TARGET = False
targets_history = []
reqb = None

display_data_from = None

target = None # current node
attribute = None # when generated via Suggester
request = None # when requested via <number>

def header ():
    print('~ KEROUAC ~')
    print('\\ Find your words, express your world.')
    print('Contact : yagomendoza.dev@gmail.com')
    print('Tip : write "help" to learn more about commands.')
    print("<!> .autosave : 'True' by default")
    print()
    
header()

while not FINISH :

    if AUTOSAVE_FEATURE:
        Database.save()
        N_CHANGES_YET = 0

    if not SUGG_MODE:
        if target!= None:
            NEW_TARGET = False if Database.find(target)!=None else True
        field_string = 'attribute_field' if not FIELD else FIELD
        target_string = "current_node" if not target else '_'.join(target.split(' '))
        target_string = ('~' if NEW_TARGET else '') + target_string
        PS1 = f"{get_time()} ~ [{field_string}]@[{target_string}]/: "
    else:
        PS1 = f" · {attribute} : "
 
    command = input(PS1).strip()

    if command == '.save':
        if not AUTOSAVE_FEATURE:
            if N_CHANGES_YET != 0:
                Database.save()
                clear_screen()
                print('-----------------------------------------'+'-'*len(str(N_CHANGES_YET)))
                print(f"The {N_CHANGES_YET} changes have been succesfully saved.")
                N_CHANGES_YET = 0
                input('>> Press ENTER to go BACK : ')
                clear_screen()
            else:
                print('<i> No changes have been performed yet.')
        else:
            print('<i> As long as autosave is enabled, there will be no changes to save.')
        continue

    if command == 'help':

        clear_screen()

        print("\n######################################################################################################################################\n")
        print("COMMANDS HANDBOOK\n")
        print(" 1) BASIC ------------------------------------------------------------------------------------------------------------------------------")
        print(" Basic set of commands to navigate through the database.")
        print(" |  e/y/o            :  switches 'attribute field' to synonyms/semantics/observations")
        print(" |  cd <title>       :  sets 'current node' to <title> node")
        print(" |  r (--pinned)     :  sets 'current node' to a random node")
        print(" |  cd ..(/../..)    :  sets 'current node' to the previous one (stackable)")
        print(" |  .remove          :  deletes the 'current node' from the database")
        print(" |  p                :  pins the 'current node'")
        print(" |  u                :  unpins the 'current node'")
        print(" |  [custom text]    :  custom text will be associated to the working 'attribute field' for the 'current node'")
        print(" |  = <i> <i> ...    :  updated the attributes for the current 'attribute field' with those of the <i> attribute")
        print(" |  <i> <i> ... =    :  transfers the 'attribute field' attributes of the 'current node' to those at <i> positions")
        print(" |  ls / +           :  (d) displays the set 'attribute field' for the current node")
        print(" 2) BATCH (b) --------------------------------------------------------------------------------------------------------------------------")
        print(" The BATCH is a space for storing nodes, either for bulk editing operations or for performing searches.")
        print(" |  <                :  (b) adds the 'current node' to the BATCH")
        print(" |  < <title>        :  (b) adds a given <title> to the BATCH")
        print(" |  > <i> <i> ...    :  (b) empties the specified nodes from the BATCH")
        print(" |  >>               :  (b) empties the BATCH completely")
        print(" |  b (sort)         :  (b) display the BATCH")
        print(" |  *<n>             :  effectuates a search basing on at least 'n' BATCH attributes")
        print(" 3) SUGGESTER --------------------------------------------------------------------------------------------------------------------------")
        print(" It allows to quickly navigate through intelligent attributes, allowing further study or inmediate insert. Therefore,")
        print(" the commands below a re applied over 'suggestions'.")
        print(" |  s                :  instantiates a suggester and accesses it")
        print(" |                   :  generates next suggestion")
        print(" |  t                :  associates current suggestion with the 'current node' through the set 'attribute field'")
        print(" |  cd               :  sets the current suggestion to 'current node'")
        print(" |  <                :  adds the suggestion to BATCH")
        print(" |  c                :  prints out the 'current node' expression")
        print(" |  ls / + (sort)    :  (d) displays the set 'attribute field' for the suggestion (purely optical)")
        print(" |  q                :  quits suggester mode")
        print(" 4) OTHER COMMANDS ---------------------------------------------------------------------------------------------------------------------")
        print(" Flow control commands, parameter toggling and txt handling actions.")
        print(" |  ~ <title>        :  finds and displays grammatically similar nodes")
        print(" |  &pinned (sort)   :  displays all favourite (pinned) nodes")
        print(" |  $obs             :  generates a random observation")
        print(" |  :ncol <n>        :  sets the number of displaying columns to <n>")
        print(" |  :autosave (0/1)  :  toggles between auto-save and manual-save")
        print(" |  :details (0/1)   :  toggles between showing details (number of connections) when displaying node lists or not")
        print(" |  .clear           :  clears the window")
        print(" |  .extract         :  saves a copy of the database to the desktop environment")
        print(" |  .save            :  saves the progress so far")
        print(" |  .exit            :  quits the terminal (discards any unsaved changes)")
        print(" 5) ATTRIBUTE DISPLAYS (d) -------------------------------------------------------------------------------------------------------------")
        print(' Before expiring (bash will report it), attribute displays (ls) implement the following commands:')
        print(" |  cd <i>           :  sets current node to specified attribute")
        print(" |  del <i> <i> ...  :  deletes the specified connexions")
        print(" |  ls / + <i>       :  displays the 'attribute field' for <i> attribute, streamlining navigation")
        print(" |  del              :  dels all attributes from the 'attribute field' at 'current node'")
        print(" |  < <i> <i> ...    :  (b) adds the specified connexions to the BATCH")
        print("########################################################################################################################################")
        input('>> Press ENTER to go BACK : ')
        clear_screen()
        continue

    if command.startswith(':details'):
        try:
            togg = [el.strip() for el in command.split(' ') if el][1]
            DETAILS_FEATURE = False if togg == '0' else True
        except:
            DETAILS_FEATURE = False if DETAILS_FEATURE else True
        print(f"<i> ['%Y/%E/%O'] format set to {DETAILS_FEATURE}.")
        continue

    if command.startswith(':autosave'):
        try:
            togg = [el.strip() for el in command.split(' ') if el][1]
            AUTOSAVE_FEATURE = False if togg == '0' else True
        except:
            AUTOSAVE_FEATURE = False if AUTOSAVE_FEATURE else True
        print(f"<i> Autosave set to {AUTOSAVE_FEATURE}.")
        continue

    if command.startswith('ls') or command.startswith('+'):

        if 'sort' in command:
            sort_flag = True
        else:
            sort_flag = False

        request = None
        if attribute != None:
            request = attribute
            display_data_from = 'attribute'
        else:
            if target != None:
                request = target
                display_data_from = 'target'
        if request == None:
            print("<!> Error 201 : no node set as current yet.")
            continue

        ls_target = target
            
        try:
            n=int(command.split(' ')[1])
            if n<=len(reqb)-1:
                ls_target = reqb[n]
            else:
                print('<!> Error 401 : specified indexes out of range.')
                continue
        except:
            pass
        
        if FIELD != None:
            try:
                left_margin = 3 if display_data_from == 'attribute' else 0
                if FIELD == "synonyms":
                    request = attribute if SUGG_MODE else ls_target
                    reqb = Database.find(request).synonyms
                    reqb = sorted(reqb) if sort_flag else reqb
                    to_print_reqb = [ent + (f" [{len(Database.find(ent).synonyms)}/{len(Database.find(ent).semantics)}/{len(Database.find(ent).observations)}]" if DETAILS_FEATURE else '') for ent in reqb]
                    if to_print_reqb == []:
                        print('<i> No content found.')
                    else:
                        utils.column_print(to_print_reqb,NCOL,left_margin)
                if FIELD == "semantics":
                    request = attribute if SUGG_MODE else ls_target
                    reqb = Database.find(request).semantics
                    reqb = sorted(reqb) if sort_flag else reqb
                    to_print_reqb = [ent + (f" [{len(Database.find(ent).synonyms)}/{len(Database.find(ent).semantics)}/{len(Database.find(ent).observations)}]" if DETAILS_FEATURE else '') for ent in reqb]
                    if to_print_reqb == []:
                        print('<i> No content found.')
                    else:
                        utils.column_print(to_print_reqb,NCOL,left_margin)
                if FIELD == "observations":
                    request = attribute if SUGG_MODE else target
                    reqb = Database.find(request).observations
                    reqb = sorted(reqb) if sort_flag else reqb
                    if reqb != []:
                        for i,obs in enumerate(reqb):
                            print(f"({i}) - {obs}")
                    else:
                        print('<i> No content found.')
            except:
                print('<!> Error 402 : current node cannot be found in the database yet.')
        else:
            print('<!> Error 200 : field to be set ("y"/"e"/"o").')
        continue

    if not SUGG_MODE :

        if command.startswith('&pinned'):

            sorted_flag = 'sort' in command

            favourites =[node.title for node in Database.nodes if node.pinned]
            if favourites != []:
                print(f"~ Displaying favourite nodes :)")
                to_print_favourites = [ent + (f" [{len(Database.find(ent).synonyms)}/{len(Database.find(ent).semantics)}/{len(Database.find(ent).observations)}]" if DETAILS_FEATURE else '') for ent in favourites]
                to_print_favourites = sorted(to_print_favourites) if sorted_flag else to_print_favourites
                utils.column_print(to_print_favourites,NCOL,left_margin=1)
                print("<i> No interaction is enabled.")
            else:
                print("<i> The database does not contain pinned nodes yet.")
            continue

        if command == '$obs':

            candidates = [node for node in Database.nodes if node.observations!=[]]
            if candidates == []:
                print("<i> There are no observations in the database.")
            else:
                node = random.choice(candidates)
                print(f"From : <{'_'.join(node.title.split(' '))}>")
                print('>> ' + random.choice(node.observations))
            continue

        if command.startswith('~'):
            command = command[1:].strip()
            results = Database.intelisearch(command)
            if results != []:
                print('Maybe you meant...')
            else:
                print('<i> No similarities found.')
            utils.column_print(results,NCOL)
            continue

        if command == 'p':
            if target != None:
                node = Database.find(target)
                if node.pinned == False:
                    node.pin()
                else:
                    print("<i> Node was already pinned.")
            else:
                print('<!> Error 201 : no node set as current yet.')
            continue
        
        if command == 'u':
            if target != None:
                node = Database.find(target)
                if node.pinned == True:
                    node.unpin()
                else:
                    print("<i> Node was already unpinned.")
            else:
                print('<!> Error 201 : no node set as current yet.')
            continue
            

        if command == '.clear':
            clear_screen()
            continue

        if '=' in command and not command.startswith('='):
            try:
                if command[0].isnumeric():
                    command = command.strip()[:-1]
                    index_candidate = [_.strip() for _ in command.split(' ') if _]
                    to_titles = [reqb[int(index)] for index in index_candidate]
                    if FIELD == 'synonyms':
                        synonyms = Database.find(target).synonyms
                        for i,title in enumerate(to_titles):
                            to_node = Database.find(title)
                            proffit = len([syn for syn in synonyms if syn not in to_node.synonyms])
                            choice_link = input(f"({i+1}/{len(to_titles)}) Press ENTER/(p) to transfer {proffit} connexions from current to {'_'.join(to_node.title.split(' '))} node (+{int(100*proffit/len(to_node.synonyms))}%) : ")
                            if choice_link in ["Y","y","yes","YES","Yes","Si","si","SI"]:
                                for syn in synonyms:
                                    to_node.add(synonym=syn)
                    if FIELD == 'semantics':
                        semantics = Database.find(target).semantics
                        for i,title in enumerate(to_titles):
                            to_node = Database.find(title)
                            proffit = len([sem for sem in semantics if sem not in to_node.semantics])
                            choice_link = input(f"({i+1}/{len(to_titles)}) Insert 'Y' to transfer {proffit} connexions from current to {'_'.join(to_node.title.split(' '))} node (+{int(100*proffit/len(to_node.synonyms))}%) : ")
                            if choice_link in ["Y","y","yes","YES","Yes","Si","si","SI"]:
                                for sem in semantics:
                                    to_node.add(sem=sem)
                    if FIELD == 'observations':
                        print("<!> Error 406 : observations cannot be assigned in bulk.")
                        continue
                    print('Finished.')
            except:
                print('<!> Error 401 : specified indexes out of range.')
            continue


        if command.startswith('='):
            candidates = [_.strip() for _ in command.split(' ')[1:] if _]

            for i,from_title_idx in enumerate(candidates):

                try:

                    from_title = reqb[int(from_title_idx)]
                    from_node = Database.find(from_title)
                    if FIELD == 'synonyms':
                        from_node_attrs = from_node.synonyms
                        target_attrs = Database.find(target).synonyms
                        proffit = int(len([x for x in from_node_attrs if x not in target_attrs])/len(from_node_attrs)*100)
                        link_choice = input(f"({i}/{len(candidates)}) Insert 'y' to transfer {len(from_node_attrs)} connexions from {'_'.join(from_node.title.split(' '))} to current node ({proffit}%) : ")
                        if link_choice in ["Y","y","yes","YES","Yes","Si","si","SI"]:
                            for synonym in Database.find(from_title).synonyms:
                                Database.find(target).add(synonym=synonym)
                            print('Done.')
                        else:
                            print('Aborted.')

                    if FIELD == 'semantics':
                        from_node_attrs = from_node.semantics
                        target_attrs = Database.find(target).semantics
                        proffit = int(len([x for x in from_node_attrs if x not in target_attrs])/len(from_node_attrs)*100)
                        link_choice = input(f"({i}/{len(candidates)}) Insert 'y' to transfer {'_'.join(from_node.title.split(' '))} {len(from_node_attrs)} connexions ({proffit}%) to current node : ")
                        if link_choice in ["Y","y","yes","YES","Yes","Si","si","SI"]:
                            for semantic in Database.find(from_title).semantics:
                                Database.find(target).add(semantic=semantic)
                            print('Done.')
                        else:
                            print('Aborted.')

                    if FIELD == 'observations':
                        print("<!> Error 406 : observations cannot be assigned in bulk.")
                        continue
                except:
                    print('<!> Error 401 : specified indexes out of range.')
            print('Finished.')
            continue

        if command.startswith('del'):
            if command == 'del':
                to_del = reqb
                for word in to_del:
                    if FIELD == "synonyms":
                        Database.find(request).delete(synonym=word)
                    if FIELD == "semantics":
                        Database.find(request).delete(semantic=word)
                    if FIELD == "observations":
                        Database.find(request).delete(observation=word)
                    N_CHANGES_YET += 1
            else:
                try:
                    idxs = [el.strip() for el in command.split(' ')][1:]
                    to_del = [reqb[int(idx)] for idx in idxs]
                    for word in to_del:
                        if FIELD == "synonyms":
                            Database.find(request).delete(synonym=word)
                        if FIELD == "semantics":
                            Database.find(request).delete(semantic=word)
                        if FIELD == "observations":
                            Database.find(request).delete(observation=word)
                        N_CHANGES_YET += 1
                    print('The following connexions have been broken:')
                    utils.column_print(to_del,NCOL)
                except:
                    print("<!> Error 401 : specified indexes out of range.")
            continue

        if command == '.extract':
            try:
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
                db = utils.extract_data_from_txt()
                now = datetime.datetime.now()
                utils.save_data_to_txt(db,file=os.path.join(desktop,f"{now.strftime('%y%m%d-%H%M%S')}.txt"))
            except:
                print('<!> Error 505 : could not save database to desktop path.')
            continue

        elif command in ('y','e','o'):
            if command == 'y':
                FIELD = "synonyms"
            elif command == 'e':
                FIELD = "semantics"
            elif command == 'o':
                FIELD = "observations"
            continue

        if command == '>>':
            empty_batch_choice = input(f"¿Are you sure you want to clear the BATCH variable ({len(BATCH)} elements)?[Y/N]\n>> ")
            if empty_batch_choice in ('Y','y','YES','yes','Yes','Si','si'):
                BATCH = []
                print('Done.')
            else:
                print('Aborted.')
            continue
            
        if command.startswith('>'):
            args = [_.strip() for _ in command.split(' ')[1:] if _.strip() != '']
            if args != []:
                els_to_delete = [BATCH[int(arg)] for arg in args]
                for el in els_to_delete:
                    BATCH.remove(el)
            continue

        if command.startswith('b ') or command == 'b':
            sorted_flag = 'sort' in command
            if BATCH != []:
                print(f"~ Displaying BATCH at {datetime.datetime.now().strftime('%H.%M.%S')}")
                to_print_batch = [ent + (f" [{len(Database.find(ent).synonyms)}/{len(Database.find(ent).semantics)}/{len(Database.find(ent).observations)}]" if DETAILS_FEATURE else '') for ent in BATCH]
                to_print_batch = sorted(to_print_batch) if sorted_flag else to_print_batch
                utils.column_print(to_print_batch,NCOL)
                print("<i> No interaction is enabled.")
            else:
                print('<i> BATCH variable is still empty.')
            continue

        if command.startswith('<'):
            
            idxs = [el.strip() for el in command.split(' ')][1:]

            if idxs != []:

                if reqb != None:
                    try:
                        if idxs[0].isnumeric():
                            elected = [reqb[int(idx)] for idx in idxs]
                            BATCH = list(set(BATCH+elected))
                        else:
                            BATCH = list(set(BATCH+[idxs[0]]))
                    except:
                        print('<!> Error 401 : specified indexes out of range.')
                else:
                    word = ' '.join(idxs)
                    if Database.find(word)!=None:
                        if word not in BATCH:
                            BATCH.append(word)
                    else:
                        print('<!> Error 303 : the inserted node does not exist.')

            else:

                if target != None:
                    BATCH = list(set(BATCH+[target]))
                else:
                    print('<!> Error 201 : no node set as current yet.')
       
            continue

        if command.startswith('cd ') and (command not in ('cd ..','cd..') and '../' not in command):
            
            new_target = ' '.join(command.split(' ')[1:])
            if new_target.isnumeric() or (new_target[0]=='-' and new_target[1].isnumeric()):
                if FIELD != 'observations':
                    if reqb != None:
                        new_target = reqb[int(new_target)]
                        if new_target != target:
                            target = new_target
                            targets_history.append(target)
                    else:
                        print('<!> Error 300 : data-pointer expired recently and indexes are no longer callable.')
                else:
                    print("<!> Error 407 : observations cannot be accessed like nodes.")
            else:
                if reqb != None:
                    if reqb != []:
                        print(f"<i> Data-pointer expired. Attributes indexes are no longer callable.")
                    reqb, request = None, None # forgets all data about the last "ls" request if the command is not in the group of the above
                if new_target != target:
                    target = new_target
                    targets_history.append(target)
            NEW_TARGET = False if Database.find(target)!=None else True
            
            continue
        
        if request != None and command not in ('.exit','.save'):
            if reqb != None:
                if reqb != []:
                    print(f"<i> Data-pointer expired. Attributes indexes are no longer callable.")
                reqb, request = None, None # forgets all data about the last "ls" request if the command is not in the group of the above
        
        if command.startswith('*'):
            try:
                results = Database.intersection(BATCH, int(command[1:].strip()))
                if results != []:
                    print(f"~ Displaying search results at {datetime.datetime.now().strftime('%H.%M.%S')}")
                    to_print_results = [ent + (f" [{len(Database.find(ent).synonyms)}/{len(Database.find(ent).semantics)}/{len(Database.find(ent).observations)}]" if DETAILS_FEATURE else '') for ent in results]
                    utils.column_print(to_print_results,NCOL,left_margin=1)
                    print("<i> No interaction is enabled.")
                else:
                    print('<i> In total, 0 results were found.')
            except:
                print('<!> Error 403 : the flexibility parameter for the search must be numeric and unique.')
            continue

        if 'cd ..' in command or 'cd..' in command:
            try:
                for _ in range(command.count('..')):
                    if len(targets_history)==1:
                        print('<!> Error 301 : history is empty.')
                    else:
                        targets_history = targets_history[:-1]
                        target = targets_history.pop(-1)
                        targets_history.append(target)
            except:
                print('<!> Error 301 : history is empty.')
            continue

        if command in ['.exit','.EXIT']:
            if N_CHANGES_YET:
                exit_choice = input(f"Found {N_CHANGES_YET} changes unsaved. Do you want to save them?[Y/N]\n>> ")
                if exit_choice in ('Y','y','YES','yes','Yes','Si','si'):
                    Database.save()
                    N_CHANGES_YET = 0
            FINISH = True
            continue

        if command == '.remove':
            if target != None:
                if Database.find(target)!=None:
                    remove_node_choice = input(f"¿Are you sure you want to remove '{'_'.join(target.split(' '))}' node?[Y/N]\n>> ")
                    if remove_node_choice in ('Y','y','YES','yes','Yes','Si','si'):
                        Database.delete_node(target)
                        target = None
                        print('Done.')
                        N_CHANGES_YET += 1
                    else:
                        print('Aborted.')
                else:
                    print('<!> Error 302 : node is not yet in the database.')
            else:
                print('<!> Error 201 : no node set as current yet.')
            continue

        if command == "r" or command.startswith('r ') : # random node
            pinned = False
            if '--pinned' in command:
                nodes = [node for node in Database.nodes if node.pinned]
                if nodes == []:
                    print('<i> There are no pinned nodes in the database.')
                    continue
                else:
                    target = random.choice(nodes).title
            else:
                target = Database.get().title
            NEW_TARGET = False
            targets_history.append(target)
            continue
        
        elif command == '':
            continue

        if command.startswith(':ncol'):
            try:
                NCOL = int([_.strip() for _ in command.split(' ') if _][-1])
            except:
                print('<!> Error 400 : check your syntax.')
            continue

        elif not target:
            print('<!> Error 201 : no node set as current yet.')
            continue

        elif command == 's':
            if FIELD not in ("synonyms","semantics"):
                print('<!> Error 202 : undetermined suggester ("y"/"e").')
                continue
            else:
                SUGG_MODE = True
                if FIELD == "synonyms":
                    Suggester = Database.ySuggester(target)
                    print(f"// Found {len(Suggester.keys)} results.")
                    SUGG_MODE = True
                elif FIELD == "semantics":
                    Suggester = Database.eSuggester(target)
                    print(f"// Found {len(Suggester.keys)} results.")
                    SUGG_MODE = True
                
                attribute = Suggester.suggest()
                if attribute == None:
                    SUGG_MODE = False
                    continue
                PS1 = f" · {attribute} : "
            continue

        else:
            if FIELD == None:
                print('<!> Error 200 : field to be set ("y"/"e"/"o").')
                continue
            else:
                if len(command) == 1:
                    print('<!> Error 404 : attributes must be at least 2 characters long.')
                else:
                    if command not in ['cd','del','ncol','CD','DEL','NCOL']:
                        if command[0].isupper():
                            EDITED = True
                            synonym,semantic,observation = None,None,None
                            if FIELD == "synonyms":
                                if len(command)>50:
                                    choice_obs = input("<i> Are you sure you are entering the attribute in the correct category?[Y/N]\n>> ")
                                    if choice_obs in ['y','Y','yes','YES','Yes','si','SI','Si']:
                                        print('Done.')
                                    else:
                                        print('Aborted.')
                                        continue
                                synonym = command
                            if FIELD == "semantics":
                                if len(command)>50:
                                    choice_obs = input("<i> Are you sure you are entering the attribute in the correct category?[Y/N]\n>> ")
                                    if choice_obs in ['y','Y','yes','YES','Yes','si','SI','Si']:
                                        print('Done.')
                                    else:
                                        print('Aborted.')
                                        continue
                                semantic = command
                            if FIELD == "observations":
                                if len(command)<50:
                                    choice_obs = input("<i> Are you sure you are entering the attribute in the correct category?[Y/N]\n>> ")
                                    if choice_obs in ['y','Y','yes','YES','Yes','si','SI','Si']:
                                        print('Done.')
                                    else:
                                        print('Aborted.')
                                        continue
                                observation = command
                            if Database.find(target) == None:
                                Database.add_node(target)
                            Database.find(target).add(synonym,semantic,observation)
                            N_CHANGES_YET += 1
                        else:
                            print('<!> Error 405 : first character must always be capitalized.')
            continue

    if SUGG_MODE:
        
        if command == 'q':
            SUGG_MODE = False
            continue
        
        elif command == '':
            attribute = Suggester.suggest()
            continue

        elif command == '<':
            BATCH.append(attribute)
            attribute = Suggester.suggest()
            continue
            
        # elif command.startswith('<'):
        #     idxs = [el.strip() for el in command.split(' ')][1:]
        #     print(idxs)

        #     if idxs != []:

        #         if idxs[0].isnumeric():
        #             elected = [reqb[int(idx)] for idx in idxs]
        #             print(elected)
        #             BATCH = list(set(BATCH+elected))
        #         else:
        #             BATCH = list(set(BATCH+[idxs[0]]))
        #     continue


        # elif command.startswith('del'):
        #     try:
        #         idxs = [el.strip() for el in command.split(' ')][1:]
        #         to_del = [reqb[int(idx)] for idx in idxs]
        #         for word in to_del:
        #             if FIELD == "synonyms":
        #                 Database.find(request).delete(synonym=word)
        #             if FIELD == "semantics":
        #                 Database.find(request).delete(semantic=word)
        #             if FIELD == "observations":
        #                 Database.find(request).delete(observation=word)
        #             N_CHANGES_YET += 1
        #     except:
        #         print("<!> Error 401 : specified indexes out of range.")
        #     continue
        #  no queremos hacer del de una suggestion nunca, osea eske qué estamos borrand oajajaj nada

        elif command == 'cd':
            if attribute != target:
                target = attribute
                NEW_TARGET = False if Database.find(target)!=None else True
                targets_history.append(target)
                SUGG_MODE = False
            continue

        elif command.startswith('cd '):
            target = ' '.join(command.split(' ')[1:])
            if target.isnumeric():
                if FIELD != 'observations':
                    target = reqb[int(target)]
                    targets_history = targets_history[:-1]
                else:
                    print("<!> Error 407 : observations cannot be accessed like nodes.")
                    continue
            targets_history.append(target)
            SUGG_MODE = False
            NEW_TARGET = False if Database.find(target)!=None else True
            continue

        elif command == 'c':
            print(f" <i> The present node is '{'_'.join(target.split(' '))}'")

        elif command == 't':
            if FIELD == None:
                continue
            else:
                synonym,semantic,observation = None,None,None
                if FIELD == "synonyms":
                    synonym = attribute
                elif FIELD == "semantics":
                    semantic = attribute
                elif FIELD == "observations":
                    observation = attribute
                if Database.find(target) == None:
                    Database.add_node(target)
                Database.find(target).add(synonym,semantic,observation)
                N_CHANGES_YET += 1
            attribute = Suggester.suggest()
            continue

        else:
            print('   <!> Error 400 : invalid command.')
            continue

