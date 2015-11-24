class EtlSchemaElement(object):
   '''Represents the type of a field (probably not mutable)'''
    def __init__(self, header=None):
        self.__header = header


class StringElement(EtlSchemaElement):
    '''Holds a simple string'''
    def __init__(self, header=None, max_length=1024):
        super(EtlSchemaElement, self).__init__(
            header=header)
        self.__max_length = max_length


class IntElement(EtlSchemaElement):
    '''Holds a simple string'''
    def __init__(self, header=None):
        super(EtlSchemaElement, self).__init__(
            header=header)


class EtlSchema(object):
    '''Base'''



class PersonSchema(EtlSchema):
    '''A person'''
    first_name = StringElement(header='First Name')
    last_name = StringElement(header='Last Name')
    nick = StringElement(header='Nickame')
    age = IntElement(header="Age")


class EmployeeSchema(PersonSchema):
    '''An employee'''
    del age
    department = StringElement


if __name__ == '__main__':

    employees = EmployeeSchema()
    print str(employee.first_name)



