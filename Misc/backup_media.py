#!/urs/bin/env python3
import sys, re, time, argparse, os, math
import sqlite3, shutil
from subprocess import Popen, PIPE
from datetime import datetime
from pathlib import Path
import shutil
import hashlib
"""
todo: use DB-APIs parameter substitution: https://docs.python.org/3/library/sqlite3.html

"""

# global variables
current_date_object = datetime.now()
verbose =  0
table_columns = {}
server_projects = []
backup_projects = []
file_operations = {}

def argparser_str_to_bool(s):
    """Convert string to bool (in argparse context)."""
    if s.lower() not in ['true', 'false']:
        raise ValueError('Need bool; got %r' % s)
    return {'true': True, 'false': False}[s.lower()]

def add_boolean_argument(parser, name, default=False, help=""):
    """Add a boolean argument to an ArgumentParser instance."""
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--' + name, nargs='?', default=default, const=True, type=argparser_str_to_bool, help=help)
    group.add_argument('--no' + name, dest=name, action='store_false')

def from_date_object_to_string(input_date_object):
    return str(input_date_object.strftime('%Y-%m-%d %H:%M:%S'))

def from_date_object_to_filename_string(input_date_object):
    return str(input_date_object.strftime('%Y%m%d_%H%M%S'))

def from_string_to_date_object(input_string):
    return datetime.strptime(input_string,'%Y-%m-%d %H:%M:%S')

def convertToInteger(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16)

def create_table(db_connection,table_name,column_name,column_type):
    """
    check if table with name table_name exists
    if not, create table with name table_name and column column_name and type column_type as primary key
    """
    c = db_connection.cursor()
    try:
        sql_string = 'CREATE TABLE {table} ({column_name} {column_type} PRIMARY KEY)'.format(table=table_name,column_name=column_name,column_type=column_type.upper())
        c.execute(sql_string)
        if verbose > 2:
            print('Creating table with sql command \"{sql}\".'.format(sql=sql_string))
    except sqlite3.Error as err:
        if verbose > 2:
            print("{0}".format(err))
    c.close()
    return 0

def create_colum(db_connection,table_name,column_name,column_type,column_default):
    """
    check if column with name column_name in table table_name exists
    if not, create column with name column_name and type column_type and default column_default in table table_name
    """
    c = db_connection.cursor()
    try:
        sql_string = 'ALTER TABLE {table} ADD COLUMN \'{column_name}\' {column_type} DEFAULT \'{column_default}\''.format(table=table_name,column_name=column_name,column_type=column_type.upper(),column_default=column_default)
        c.execute(sql_string)
        if verbose > 2:
            print('Creating table with sql command \"{sql}\".'.format(sql=sql_string))
    except sqlite3.Error as err:
        if verbose > 2:
            print("{0}".format(err))
    c.close()
    return 0

def index_in_column_list(colum_list,column_name):
    """

    return index of column_name in column_list for sql selection
    add 1 for primary key 'id' omitted from column_list

    """
    try:
        index = column_list.index(column_name)
        return index+1
    except:
        print('Column {name} could not be found in list \'{list}\''.format(name=column_name,list='\',\''.join(colum_list)))
        sys.exit(1)

def open_db_file(db_file_name):
    """
    open db file name and ensure that it conforms to schema
    if not, update schema
    """
    print('Opening DB file: \"%s\"' % db_file_name)

    conn = sqlite3.connect(db_file_name)

    # table media
    # field id: hash of name, type TEXT
    # field name: name of media, type TEXT
    # field capacity: capacity of media[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    global table_columns
    table_columns['media'] = ['name','capacity','free','last_update']
    create_table(conn,'media','id','integer')
    create_colum(conn,'media','name','text','')
    create_colum(conn,'media','capacity','integer',0)
    create_colum(conn,'media','free','integer',0)
    create_colum(conn,'media','last_update','text','')

    # table server_files
    # field id: hash of name, type TEXT
    # field media_id: key from media table, type TEXT
    # field name: name of media file including project name, type TEXT
    # field size: size[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    table_columns['server_files'] = ['media_id','name','project','filename','size','last_update']
    create_table(conn,'server_files','id','integer')
    create_colum(conn,'server_files','media_id','text','')
    create_colum(conn,'server_files','name','text','')
    create_colum(conn,'server_files','project','text','')
    create_colum(conn,'server_files','filename','text','')
    create_colum(conn,'server_files','size','integer',0)
    create_colum(conn,'server_files','last_update','text','')

    # table backup_files
    # field id: hash of name, type TEXT
    # field media_id: key from media table, type TEXT
    # field name: name of media file including project name, type TEXT
    # field size: size[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    table_columns['backup_files'] = ['media_id','name','project','filename','size','last_update']
    create_table(conn,'backup_files','id','integer')
    create_colum(conn,'backup_files','media_id','text','')
    create_colum(conn,'backup_files','name','text','')
    create_colum(conn,'backup_files','project','text','')
    create_colum(conn,'backup_files','filename','text','')
    create_colum(conn,'backup_files','size','integer',0)
    create_colum(conn,'backup_files','last_update','text','')

    return conn

def close_db(db_file_connection):
    c = db_file_connection.cursor()
    c.execute('pragma database_list')
    db_location_name = c.fetchall()[0][2]
    db_file_connection.commit()
    db_file_connection.close()
    print('Committing and closing DB file: \"%s\"' % db_location_name)
    return 0

def get_id_for_media(connection,media_name):
    """
    for a given media_name, check the id in the media table
    if the media does not have an entry, create it
    """
    # generate media id from media_name
    generated_media_id = convertToInteger(media_name)

    # gather free space on media_name
    total, used, free = shutil.disk_usage(media_name)
    # for zfs volumes, total is not correct, use zpool status command to get total
    if total == used+free:
        # this is a zfs volume
        process = Popen(['zpool', 'list', '-pH', '-o', 'size', media_name.replace('/Volumes','').replace('/','')], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        total = int(stdout.strip())
    update_row_in_table(connection,'media',generated_media_id, {'name': media_name, 'capacity': total, 'free': free, 'last_update': from_date_object_to_string(current_date_object)})

    if verbose > 1:
        print("Media id of media name \"{media_name}\" is \"{media_id}\".".format(media_name=media_name,media_id=generated_media_id))

    return generated_media_id

def update_info_for_media(connection, id, media_name, capacity, free):
    """
        update information for media id
    """

    update_row_in_table(connection, \
                        'media',id, \
                        { 'media_name': media_name, \
                        'capacity': capacity, \
                        'free': free, \
                        'last_update': from_date_object_to_string(current_date_object)})


def get_info_for_media(connection,media_name):
    """
    return all info for media_name: (id, name, capacity, free, last_update)
    """

    c = connection.cursor()
    try:
        sql_string = 'SELECT * FROM media WHERE name=\'{name}\''.format(name=media_name)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    if len(all_rows) > 1:
        print("Problem: more than 1 entry for media: {media_name}".format(media_name=media_name))
        print("all_rows: ")
        print(all_rows)
        sys.exit(1)

    return (all_rows[0][0],all_rows[0][1],all_rows[0][2],all_rows[0][3],all_rows[0][4])

def get_media_name_for_media_id(connection,media_id):
    """
    return media_id for media_name from media table
    """

    c = connection.cursor()
    try:
        sql_string = 'SELECT name FROM media WHERE id={id}'.format(id=media_id)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    if len(all_rows) != 1 :
        print("Problem: more than 1 or no entry for media id: {id}".format(id=media_id))
        print("all_rows: ")
        print(all_rows)
        sys.exit(1)

    return all_rows[0][0]


def update_row_in_table(connection,table_name,id,row_values):
    """

    update row in table:
    if id exists in table and last_update in table < last_update in input, update all table values
    if id does not exist, add to table

    """

    sql_update_column_string = ''
    sql_insert_column_string = ''
    for column_name in table_columns[table_name]:
        sql_update_column_string += '{name}=?, '.format(name=column_name)
        sql_insert_column_string += '?, '
    sql_update_column_string = sql_update_column_string[:-2]
    sql_insert_column_string = sql_insert_column_string[:-2]
    column_value_list = list(row_values.values())

    c = connection.cursor()
    try:
        # try inserting new row; if id already exists, update row if update_date in db is older than update_date in row_values
        sql_string = 'insert into {table} ({columns}) values ({column_values})'.format(table=table_name, columns=','.join(['id'] + table_columns[table_name]),column_values='?, ' + sql_insert_column_string)
        tuple = [str(id)] + column_value_list
        c.execute(sql_string,tuple)
        if verbose > 2:
            print('Inserting into table with sql command \"{sql}\" and values \'{values}\'.'.format(sql=sql_string, values='\',\''.join(map(str,tuple))))
    except sqlite3.IntegrityError:
        # update row if update_date in db is older than update_date in row_values
        sql_string = 'update {table} set {columns} where id=?'.format(table=table_name,columns=sql_update_column_string)
        tuple = column_value_list+[id]
        c.execute(sql_string,tuple)
        if verbose > 2:
            print('Updating in table with sql command \"{sql}\" and values \'{values}\'.'.format(sql=sql_string, values='\',\''.join(map(str,tuple))))
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
        print('Problem updating table \'{table}\' for id \'{key}\' with values \'{values}\''.format(table=table_name, key=id, values=row_values))
        sys.exit(1)

    c.close()
    return 0

def update_from_directory(connection,top_directory,project_list,table_name):
    """
    update the database from the connection with all media files in the project_list in the top_directory
    """

    print("Updating information from top_directory: \'{top_directory}\'.".format(top_directory=top_directory))
    if os.path.exists(top_directory) == False:
        print('Top directory" {top_directory} does not exist (media not mounted?). Aborting update from directrory.'.format(top_directory=top_directory))
        return False

    # which projects are being considered
    print("Project list: \'{project_list}\'".format(project_list='\', \''.join(map(str,project_list))))

    # get id of media from media table
    media_id = get_id_for_media(connection,top_directory)

    # loop over files in directory and gather all needed information
    filelist = {}
    counter = {}
    for project in project_list:
        counter[project] = 0
        for (root, dirs, files) in os.walk(top_directory + '/' + project):
            if root.find('.tmp') > 0 or root.find('.') < 0:
                for item in files:
                    if item[0] != '.':
                        tmp_file = root + '/' + item
                        file = tmp_file.replace(top_directory + '/' + project + '/','')
                        # exclude dot files
                        if file[0:4] == '.tmp' or file[0] != '.':
                            # attention, all files on backup media have _Ext added to their project, remove here and add again if necessary, but store real value
                            name = project.replace('_Ext','') + '/' + file
                            id = convertToInteger(name)
                            size = os.path.getsize(root + '/' + item)
                            filelist[id] = {'name' : name, 'project': project, 'filename': file, 'size' : size}
                            counter[project] += 1

    if verbose > 0:
        for project in project_list:
            print("Project: \'{project}\': number of files: {numfiles}.".format(project=project, numfiles=counter[project]))

    # add entries to files table
    for file_id in filelist.keys():
        update_row_in_table(connection, \
                            table_name,file_id, \
                            { 'media_id': media_id, \
                            'name': filelist[file_id]['name'], \
                            'project': filelist[file_id]['project'], \
                            'filename': filelist[file_id]['filename'], \
                            'size': filelist[file_id]['size'], \
                            'last_update': from_date_object_to_string(current_date_object)})

    # find entries in files table that have not be update_date
    # these files were removed from the top_directory
    # remove them from the files table
    clean_outdated_entries(connection,top_directory,project_list,table_name,media_id)

def clean_outdated_entries(connection,top_directory,project_list,table_name,media_id):
    """
    query the files table for entries with date < current_date
    """

    c = connection.cursor()
    try:
        sql_string = 'SELECT * FROM {table} WHERE last_update < DATETIME(\'{current_date}\') AND media_id={media_id}'.format(table=table_name,current_date=from_date_object_to_string(current_date_object),media_id=media_id)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    do_all = False
    for row in all_rows:
        id = row[0]
        name = str(row[2])
        project = str(row[3])
        if project in project_list:
            print('Updating top directory \'{top_directory}\': name \'{name}\' was removed from the directory, should the entry be removed from the table \'{table}\'?'.format(top_directory=top_directory,name=name,table=table_name))
            delete = False
            answer = None
            if do_all == False:
                while answer not in ('y','n','yes','no','all'):
                    answer = input("Please enter yes or no (y or n), or all to stop asking: ")
                    if answer == 'y':
                        delete = True
                    elif answer == 'yes':
                        delete = True
                    elif answer == 'n':
                        delete = False
                    elif answer == 'no':
                        delete = False
                    elif answer == 'all':
                        do_all = True
                    else:
                        print("Please enter yes or no (y or n), or all to stop asking: ")
            if delete == True or do_all == True:
                c = connection.cursor()
                try:
                    sql_string = 'DELETE FROM {table} WHERE id = {id}'.format(id=id,table=table_name)
                    c.execute(sql_string)
                except sqlite3.Error as err:
                    print("SQLITE3 error: {0}".format(err))
                c.close()

def check_for_table_duplicates(connection,table_name):
    """
        check for duplicated filenames in a single table
    """
    c = connection.cursor()
    try:
        sql_string = 'select filename,count(filename) from {table_name} group by filename having count(filename) > 1'.format(table_name=table_name)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    if len(all_rows) > 0:
        print("\nFollowing duplicates have been found in table " + table_name + "\n")
        for row in all_rows:
            filename = row[0]
            c = connection.cursor()
            try:
                sql_string = 'SELECT media.name,{table_name}.id,{table_name}.project,{table_name}.filename,{table_name}.size FROM {table_name} JOIN media on {table_name}.media_id = media.id WHERE {table_name}.filename like \'%{filename}%\''.format(table_name=table_name,filename=filename)
                c.execute(sql_string)
                all_rows_2 = c.fetchall()
            except sqlite3.Error as err:
                print("SQLITE3 error: {0}".format(err))
            c.close()
            files = []
            for row2 in all_rows_2:
                media_name = row2[0]
                id = row2[1]
                project = row2[2]
                filename = row2[3]
                size = int(row2[4])
                files.append((media_name,id,project,filename,size))
            sorted_files = sorted(files,key=lambda size: size[4])
            question = 'File: {project}/{name} on media: {media} has the smallest duplicate in size, do you want to delete it? Please enter yes or no (y or n): '.format(project=sorted_files[0][2],name=sorted_files[0][3],media=sorted_files[0][0])
            delete = False
            answer = None
            while answer not in ('y','n','yes','no'):
                answer = input(question)
                if answer == 'y':
                    delete = True
                elif answer == 'yes':
                    delete = True
                elif answer == 'n':
                    delete = False
                elif answer == 'no':
                    delete = False
                elif answer == 'all':
                    do_all = True
                else:
                    print(question)
            if delete == True:
                media_name = sorted_files[0][0]
                id = sorted_files[0][1]
                project = sorted_files[0][2]
                filename = sorted_files[0][3]
                size = sorted_files[0][4]
                file_deleted = delete_file_from_external_media(connection,table_name,media_name,id,project,filename,size)
            print('')

def copy_file_to_external_media(connection,destination_table_name,media_name,id,project,filename,size):
    """
    find space for file to copy on external media
    wait for media to be mounted
    copy file
    update db
    """

    # source file check
    sourcefile = os.path.join(media_name,project,filename)
    if os.path.isfile(sourcefile) == False:
        print("Source file {sourcefile} for copy does not exist, aborting file copy.".format(sourcefile=sourcefile))
        return False

    # find space for file of size on external media, add 1GB buffer on every media
    c = connection.cursor()
    try:
        sql_string = 'SELECT id,name,capacity,free FROM media WHERE name LIKE \'%External%\' and free > {size} ORDER BY free;'.format(size=size+1000000000)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    if len(all_rows) < 1:
        print("Could not find room for file {name} of size {size} on known external media, please add empty media.".format(name=filename,size=size))
        return False

    copy_media_id = all_rows[0][0]
    copy_media_name = all_rows[0][1]
    copy_media_capacity = all_rows[0][2]
    copy_media_free = all_rows[0][3]

    # copy file
    if project.find("_Ext") > 0:
        # source file on backup media
        destination_project = project.replace("_Ext","")
    else:
        # source file on server
        destination_project = project + "_Ext"
    destinationfile = os.path.join(copy_media_name,destination_project,filename)
    # insert operation into file_operations
    if copy_media_name not in file_operations.keys(): file_operations[copy_media_name] = []
    file_operations[copy_media_name].append({"action" : "copy", "source" : sourcefile, "destination" : destinationfile})

    # update secondary table
    update_row_in_table(connection, \
                        destination_table_name,id, \
                        { 'media_id': copy_media_id, \
                        'name': os.path.join(project,filename), \
                        'project': destination_project, \
                        'filename': filename, \
                        'size': size, \
                        'last_update': from_date_object_to_string(current_date_object)})
    # update media table
    update_info_for_media(connection, copy_media_id, copy_media_name, copy_media_capacity, copy_media_free-size)
    return True

def delete_file_from_external_media(connection,table_name,media_name,id,project,filename,size):
    """
    delete filename from external media called media_name
    wait for media_name to be mounted before proceeding
    clean up database
    return True if file was deleted
    """

    file = os.path.join(media_name,project,filename)

    # insert operation into file_operations
    if media_name not in file_operations.keys(): file_operations[media_name] = []
    file_operations[media_name].append({"action" : "delete","source" : file})

    # remove from table table_name
    c = connection.cursor()
    try:
        sql_string = 'DELETE FROM {table} WHERE id = {id}'.format(id=id,table=table_name)
        c.execute(sql_string)
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()
    # update media table
    (media_id, media_name_2, capacity, free, last_updated) = get_info_for_media(connection,media_name)
    free += size
    update_info_for_media(connection, media_id, media_name, capacity, free)
    return True

def check_for_differences_and_act(connection,primary_table_name,secondary_table_name,mode):
    """
    check for entries in primary table name that do not exist in secondary table name
    mode: "delete" or "copy"
    """

    c = connection.cursor()
    try:
        sql_string = 'SELECT {primary_table_name}.id,{primary_table_name}.media_id,{primary_table_name}.name,{primary_table_name}.project,{primary_table_name}.filename,{primary_table_name}.size FROM {primary_table_name} LEFT OUTER JOIN {secondary_table_name} ON ({primary_table_name}.name = {secondary_table_name}.name) WHERE {secondary_table_name}.name IS NULL'.format(primary_table_name=primary_table_name,secondary_table_name=secondary_table_name)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    files_per_media_name = {}

    for row in all_rows:
        id = row[0]
        media_id = row[1]
        media_name = get_media_name_for_media_id(connection,media_id)
        name = row[2]
        project = row[3]
        filename = row[4]
        size = row[5]
        if media_name not in files_per_media_name.keys():
                files_per_media_name[media_name] = []
        files_per_media_name[media_name].append({'id': id, 'project': project, 'filename': filename, 'size': size})

    for local_media_name in files_per_media_name.keys():
        sorted_entries = sorted(files_per_media_name[local_media_name],key=lambda size: size['size'])
        for entry in sorted_entries:
            if mode == "delete":
                delete_file_from_external_media(connection,primary_table_name,local_media_name,entry['id'],entry['project'],entry['filename'],entry['size'])
            elif mode == "copy":
                copy_file_to_external_media(connection,secondary_table_name,local_media_name,entry['id'],entry['project'],entry['filename'],entry['size'])
            else:
                print("Mode: {mode} not available, doing nothing.")

def check_for_file_size_differences_and_delete_inconsistencies_from_backup(connection,primary_table_name,secondary_table_name):
    """
    compare file sizes between primary table and secondary table, delete from secondary table and corresponding media
    """

    c = connection.cursor()
    try:
        sql_string = 'SELECT {secondary_table_name}.id,{secondary_table_name}.media_id,{secondary_table_name}.name,{secondary_table_name}.project,{secondary_table_name}.filename,{secondary_table_name}.size FROM {primary_table_name} LEFT OUTER JOIN {secondary_table_name} ON ({primary_table_name}.name = {secondary_table_name}.name) WHERE {primary_table_name}.size != {secondary_table_name}.size'.format(primary_table_name=primary_table_name,secondary_table_name=secondary_table_name)
        c.execute(sql_string)
        all_rows = c.fetchall()
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
    c.close()

    files_per_media_name = {}

    for row in all_rows:
        id = row[0]
        media_id = row[1]
        media_name = get_media_name_for_media_id(connection,media_id)
        name = row[2]
        project = row[3]
        filename = row[4]
        size = row[5]
        if media_name not in files_per_media_name.keys():
                files_per_media_name[media_name] = []
        files_per_media_name[media_name].append({'id': id, 'project': project, 'filename': filename, 'size': size})

    for local_media_name in files_per_media_name.keys():
        sorted_entries = sorted(files_per_media_name[local_media_name],key=lambda size: size['size'])
        for entry in sorted_entries:
            # print("Deleting file: {file} from table {table}".format(file=os.path.join(local_media_name,entry['project'],entry['filename']),table=secondary_table_name))
            delete_file_from_external_media(connection,secondary_table_name,local_media_name,entry['id'],entry['project'],entry['filename'],entry['size'])

def execute_file_operations():
    if verbose > 2:
        print("Following file operations will be executed")
        for media_name in sorted(file_operations.keys()):
            print('Media {media}'.format(media=media_name))
            for operation in file_operations[media_name]:
                if operation['action'] == "delete":
                    print("Deletion of {source}".format(source=operation["source"]))
            for operation in file_operations[media_name]:
                if operation['action'] == "copy":
                    print("Copy of {source} to {destination}".format(source=operation["source"],destination=operation["destination"]))

    for media_name in sorted(file_operations.keys()):
        # check if media_name is mounted
        exists = os.path.exists(media_name)
        while exists == False:
            answer = None
            abort = False
            question = 'Please mount external media: {media} and continue with yes (y) or abort with no (n): '.format(media=media_name)
            while answer not in ('y','yes','n','no'):
                answer = input(question)
                if answer == 'y':
                    abort = False
                elif answer == 'yes':
                    abort = False
                elif answer == 'n':
                    abort = True
                elif answer == 'no':
                    abort = True
                else:
                    print(question)
            if abort == True:
                break
            else:
                exists = os.path.exists(media_name)
        if exists == False:
            # mouting of media_name aborted
            print('Operations on media {media_name} were aborted'.format(media_name=media_name))
        else:
            # execute operations, first deletions, then copy
            for operation in file_operations[media_name]:
                if operation["action"] == "delete" :
                    if verbose > 1:
                        print("Trying to delete file {source} on media {media}".format(source=operation["source"],media=media_name))
                    try:
                        os.remove(operation["source"])
                        if verbose > 0:
                            print("Deleted file {source} on media {media}".format(source=operation["source"],media=media_name))
                    except IOError as io_err:
                        if verbose > 1:
                            print("{0}".format(io_err))
                        print("Could not delete file {source} on media {media}".format(source=operation["source"],media=media_name))

            for operation in file_operations[media_name]:
                if operation["action"] == "copy" :
                    if verbose > 1:
                        print("Trying to copy file {source} to {destination} on media {media}".format(source=operation["source"],destination=operation["destination"],media=media_name))
                    try:
                        shutil.copy(operation["source"],operation["destination"])
                        if verbose > 0:
                            print("Copied file {source} to {destination} on media {media}".format(source=operation["source"],destination=operation["destination"],media=media_name))
                    except IOError as io_err:
                        os.makedirs(os.path.dirname(operation["destination"]))
                        try:
                            shutil.copy(operation["source"],operation["destination"])
                            if verbose > 0:
                                print("Copied file {source} to {destination} on media {media}".format(source=operation["source"],destination=operation["destination"],media=media_name))
                        except IOError as io_err:
                            if verbose > 1:
                                print("{0}".format(io_err))
                            print("Could not copy source {source} to destination {destination} on media {media}".format(source=operation["source"],destination=operation["destination"],media=media_name))

def main(args):
    """

    backup media to a collection of external disks
    all interaction with media is POSIX

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="count", help="Increase the verbosity level by increasing -v, -vv, -vvv", default=0)
    parser.add_argument("--central_db_file_location", action="store", default = "~/Dropbox/Private/Projects/Backup", help="Location of centrally stored db file")
    parser.add_argument("--server_media_top_directory", action="store", default = "/Media", help="Location of central server media top directory")
    parser.add_argument("--external_media_top_directory", action="store", default = None, help="Top media directory on external media")
    parser.add_argument("--db_file_name", action="store", default = "media_backup.sqlite", help="Name of media backup db file")
    parser.add_argument("--project", action="append", default = [], help="Name of a directory in the media top directory")

    add_boolean_argument(parser,"standard_mode", default=True,help="Update from both the server and external media, standard running mode")
    parser.add_argument("--update_only_from_external_media", action="store_true", default = False, help="Update the db only using information from the external media, cannot be used together with --update_only_from_server_media")
    parser.add_argument("--update_only_from_server_media", action="store_true", default = False, help="Update the db only using information from the server, cannot be used together with --update_only_from_external_media")
    parser.add_argument("--checks_only", action="store_true", default = False, help="Only perform checks which files to delete and which files to copy to backup media")
    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    standard_mode = args.standard_mode
    update_only_from_external_media = args.update_only_from_external_media
    update_only_from_server_media = args.update_only_from_server_media
    checks_only = args.checks_only
    if standard_mode == True and (update_only_from_server_media == True or update_only_from_external_media == True or checks_only == True):
        print("--update_only_from_server_media, --update_only_from_external_media or --checks_only cannot be set if standard_mode is selected (which is the default)")
        sys.exit(1)
    if update_only_from_server_media == True and update_only_from_external_media == True:
        print("--update_only_from_server_media and --update_only_from_external_media cannot be set at the same time, select standard_mode true instead (which is the default)")
        sys.exit(1)
    if standard_mode == True:
        update_only_from_server_media = True
        update_only_from_external_media = True
        checks_only = True
    if update_only_from_external_media == True and args.external_media_top_directory == None:
        print("Update from external media selected, please specify external_media_top_directory.")
        sys.exit(1)
    global server_projects
    server_projects = args.project

    # default for projects on server
    if len(server_projects) <= 0:
        server_projects = ['.Spotlight-V200','Audiobooks','Backups','Downloads','HD Movies','Home Movies','Literatur','Movies','Music','Photos','TV Shows']

    # directory on backup media has _Ext ending to avoid duplicated ZFS mounts
    # creating backup_projects
    global backup_projects
    backup_projects = []
    for project in server_projects:
        backup_projects.append(project+"_Ext")

    # create dictionary for file operations
    # key is media_name
    # value is dictionary for operation
    global file_operations
    file_operations = {}

    # clean up db file Location
    central_db_file_location = args.central_db_file_location
    if central_db_file_location.find("~") >= 0 or central_db_file_location.find('$HOME') >= 0:
        home_dir = str(Path.home())
        central_db_file_location = central_db_file_location.replace("~",home_dir)
        central_db_file_location = central_db_file_location.replace("$HOME",home_dir)
        if verbose > 2:
            print("Replaced home dir place holders in central db file location")

    # backup central db file, assume extension is .sqlite
    central_db_file_name = central_db_file_location + '/' + args.db_file_name
    backup_central_db_file_name = central_db_file_location + '/' + args.db_file_name.replace('.sqlite','_' + from_date_object_to_filename_string(current_date_object) + '.sqlite')
    try:
        shutil.copy(central_db_file_name,backup_central_db_file_name)
    except:
        if verbose > 1:
            print('WARNING: Previous SQL database file did not exist, creating new database file')

    # open db files on external media and from central location
    central_db_file_connection = open_db_file(central_db_file_name)

    # update from information from media folder on central server
    if update_only_from_server_media == True :
        update_from_directory(central_db_file_connection,args.server_media_top_directory,server_projects,'server_files')

    # update from information from media folder on external media
    if update_only_from_external_media == True :
        update_from_directory(central_db_file_connection,args.external_media_top_directory,backup_projects,'backup_files')

    if checks_only == True:
        # check for duplicates in server and backup files table_columns
        check_for_table_duplicates(central_db_file_connection,"server_files")
        check_for_table_duplicates(central_db_file_connection,"backup_files")

        # check for files that need to be deleted from the backup media because they have been removed from the server
        check_for_differences_and_act(central_db_file_connection,"backup_files","server_files","delete")
        # check for files that have different sizes on server and backup and delete files on backup to be re-copied
        check_for_file_size_differences_and_delete_inconsistencies_from_backup(central_db_file_connection,"server_files","backup_files")
        # check for files that don't have a backup yet on external media and need to be copied
        check_for_differences_and_act(central_db_file_connection,"server_files","backup_files","copy")

    # execute file Operations
    execute_file_operations()

    # close external media and central db central db files
    close_db(central_db_file_connection)

if __name__ == '__main__':
    main(sys.argv)
