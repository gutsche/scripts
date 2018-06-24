#!/urs/bin/env python3
import sys, re, time, argparse, os, math
import sqlite3, shutil
from subprocess import Popen, PIPE
from datetime import datetime
import shutil
import hashlib
"""
todo: use DB-API’s parameter substitution: https://docs.python.org/3/library/sqlite3.html

"""


# global variables
current_date_object = datetime.now()
verbose =  False
table_columns = {}

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
        c.execute('create table ? (? ? primary key)', [table_name,column_name,column_type])
        if verbose == True:
            print('Table \"%s\" not found, creating it with column \"%s\" as primary key'\
            % (table_name,column_name))
    except:
        if verbose == True:
            print('Table \"%s\" was found!'\
            % (table_name))
    c.close()
    return 0

def create_colum(db_connection,table_name,column_name,column_type,column_default):
    """
    check if column with name column_name in table table_name exists
    if not, create column with name column_name and type column_type and default column_default in table table_name
    """
    c = db_connection.cursor()
    try:
        c.execute('alter table ? add column \'?\' ? default \'?\'', [table_name,column_name,column_type,column_default])
        if verbose == True:
            print('Column \"%s\" not found in table \"%s\", creating it with type \"%s\" and default \"%s\"'\
            % (column_name,table_name,column_type,column_default))
    except:
        if verbose == True:
            print('Column \"%s\" found in table \"%s\"!'\
            % (column_name,table_name))
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
    if (verbose == True):
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

    # table files
    # field id: hash of name, type TEXT
    # field media_id: key from media table, type TEXT
    # field name: name of media file including project name, type TEXT
    # field size: size[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    table_columns['files'] = ['media_id','name','size','last_update']
    create_table(conn,'files','id','integer')
    create_colum(conn,'files','media_id','text','')
    create_colum(conn,'files','name','text','')
    create_colum(conn,'files','size','integer',0)
    create_colum(conn,'files','last_update','text','')

    return conn

def close_db(db_file_connection):
    c = db_file_connection.cursor()
    c.execute('pragma database_list')
    db_location_name = c.fetchall()[0][2]
    if (verbose == True):
        print('Committing and closing DB file: \"%s\"' % db_location_name)

    db_file_connection.commit()
    db_file_connection.close()
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
        process = Popen(['zpool', 'list', '-pH', '-o', 'size', media_name.replace('/Volumes/','')], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        total = int(stdout.strip())
    update_row_in_table(connection,'media',generated_media_id, {'name': media_name, 'capacity': total, 'free': free, 'last_update': from_date_object_to_string(current_date_object)})

    return generated_media_id

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
        if verbose == True:
            print('Inserting into table with sql command \"{sql}\" and values \'{values}\'.'.format(sql=sql_string, values='\',\''.join(map(str,tuple))))
        c.execute(sql_string,tuple)
    except sqlite3.IntegrityError:
        # update row if update_date in db is older than update_date in row_values
        sql_string = 'update {table} set {columns} where id=?'.format(table=table_name,columns=sql_update_column_string)
        tuple = column_value_list+[id]
        if verbose == True:
            print('Updating in table with sql command \"{sql}\" and values \'{values}\'.'.format(sql=sql_string, values='\',\''.join(map(str,tuple))))
        c.execute(sql_string,tuple)
    except sqlite3.Error as err:
        print("SQLITE3 error: {0}".format(err))
        print('Problem updating table \'{table}\' for id \'{key}\' with values \'{values}\''.format(table=table_name, key=id, values=row_values))
        sys.exit(1)

    c.close()
    return 0

def update_from_directory(connection,top_directory,project_list):
    """
    update the database from the connection with all media files in the project_list in the top_directory
    """

    # loop over files in directory and gather all needed information
    filelist = {}
    for project_dir in project_list:
        counter = 0
        for (root, dirs, files) in os.walk(top_directory + '/' + project_dir):
            dir = root.replace(top_directory + '/' + project_dir + '/','')
            if dir[0] != '.':
                for file in files:
                    name = project_dir + '/' + file
                    id = convertToInteger(name)
                    size = os.path.getsize(root + '/' + file)
                    filelist[id] = {'name' : name, 'size' : size}
                    counter += 1
        if verbose == True:
            print('Gathered information for %i files in project dir \"%s\"' % (counter,project_dir))

    # get id of media from media table
    media_id = get_id_for_media(connection,top_directory)
    if verbose == True:
        print('ID of external media with top directory \"%s\": %i' % (top_directory,media_id))

    # add entries to files table_name
    for file_id in filelist.keys():
        update_row_in_table(connection,'files',file_id, {'media_id': media_id,'name': filelist[file_id]['name'], 'size': filelist[file_id]['size'], 'last_update': from_date_object_to_string(current_date_object)})

def main(args):
    """

    backup media to a collection of external disks
    all interaction with media is POSIX

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--central_db_file_location", action="store", default = "/Volumes/Home/gutsche/Documents/Private/Projects/Backup", help="Location of centrally stored db file")
    parser.add_argument("--server_media_top_directory", action="store", default = "/Volumes/Media", help="Location of central server media top directory")
    parser.add_argument("--external_media_top_directory", action="store", default = None, help="Top media directory on external media", required=True)
    parser.add_argument("--db_file_name", action="store", default = "media_backup.sqlite", help="Name of media backup db file")
    parser.add_argument("--project", action="append", default = [], help="Name of a directory in the media top directory", required=True)
    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    projects = args.project
    # default for projects
    if len(projects) <= 0:
        projects = ['Movies']

    # backup central db file, assume extension is .sqlite
    central_db_file_name = args.central_db_file_location + '/' + args.db_file_name
    backup_central_db_file_name = args.central_db_file_location + '/' + args.db_file_name.replace('.sqlite','_' + from_date_object_to_filename_string(current_date_object) + '.sqlite')
    try:
        shutil.copy(central_db_file_name,backup_central_db_file_name)
    except:
        if verbose == True:
            print('WARNING: Previous SQL database file did not exist')

    # open db files on external media and from central location
    central_db_file_connection = open_db_file(central_db_file_name)

    # update from information from media folder on central server
    update_from_directory(central_db_file_connection,args.server_media_top_directory,projects)

    # close external media and central db central db files
    close_db(central_db_file_connection)

if __name__ == '__main__':
    main(sys.argv)
