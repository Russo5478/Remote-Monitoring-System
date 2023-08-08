from time import strftime
from sqlite3 import connect
import datetime
from dateutil.relativedelta import relativedelta


def get_current_time():
    current_time = strftime('%d/%B/%Y %H:%M')

    return str(current_time)


def day_string(when):
    if when.lower == 'yesterday':
        yesterday = datetime.datetime.now() - relativedelta(days=1)
        yesterday_time = format(yesterday, '%d/%B/%Y')

        return_date = str(yesterday_time + "%")

    elif when.lower == 'this_month':
        this_month = datetime.datetime.now()
        this_month_time = format(this_month, '%B/%Y')

        return_date = str("%" + this_month_time + "%")

    elif when.lower == 'last_month':
        last_month = datetime.datetime.now() - relativedelta(months=1)
        last_month_time = format(last_month, '%B/%Y')

        return_date = str("%" + last_month_time + "%")

    elif when.lower == 'this_year':
        this_year = datetime.datetime.now()
        this_year_time = format(this_year, '%Y')

        return_date = "%" + str(this_year_time) + "%"

    elif when.lower == 'last_year':
        last_year = datetime.datetime.now() - relativedelta(years=1)
        last_year_time = format(last_year, '%Y')

        return_date = "%" + str(last_year_time) + "%"

    elif when.lower == 'last_7':
        days_list = []
        for i in range(1, 8):
            day_ = datetime.datetime.now() - relativedelta(days=i)
            day_time = format(day_, '%d/%B/%Y')

            days_list.append(str(day_time) + "%")

        return_date = days_list

    else:
        return_date = None

    return return_date


def database_all_lookup(db_path: str, what_selection: str, from_selection: str):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {}".format(what_selection, from_selection)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_specified_lookup(db_path: str, what_selection: str, from_selection: str, where_selection: str,
                              value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {} WHERE {} ='{}'".format(what_selection, from_selection, where_selection,
                                                               value_select)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_like_lookup(db_path: str, what_selection: str, from_selection: str, where_selection: str, value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {} WHERE {} LIKE '{}'".format(what_selection, from_selection, where_selection,
                                                                   value_select)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result


def database_update(db_path: str, what_selection: str, set_selection: str, new_value, where_selection: str,
                    value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "UPDATE {} SET {}='{}' WHERE {}='{}'".format(what_selection, set_selection, new_value,
                                                                  where_selection, value_select)
    writer.execute(lookup_command)
    db_connection.close()


def database_delete(db_path: str, from_selection: str, where_selection: str, value_select):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "DELETE FROM {} WHERE {}='{}'".format(from_selection, where_selection, value_select)
    writer.execute(lookup_command)
    db_connection.close()


def database_insert(db_path: str, into_selection: str, new_values: tuple):
    values_length = len(new_values)
    number_of_commas = '?' * values_length
    comma_parameters = ','.join(number_of_commas[i:i + 1] for i in range(0, len(number_of_commas), 1))
    parameters = '(' + comma_parameters + ')'

    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "INSERT INTO {} VALUES {}".format(into_selection, parameters), new_values
    writer.execute(str(lookup_command))
    db_connection.close()
