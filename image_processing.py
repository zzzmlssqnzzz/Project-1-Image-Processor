MAX_WHITE_VALUE = 255

def is_valid_image(image):
    """ (list<list>) -> bool
    Takes a nested list and returns True if the nested list
    represents a non-compressed PGM image matrix.Otherwise,
    returns False.
    
    >>> is_valid_image([[1, 2, 3], [4, 5, 6], [7, 8, 255]])
    True
    
    >>> is_valid_image([[1, 3], [4, 10, 6]])
    False
    
    >>> is_valid_image([["hello", "my"],["friend", "I"],["miss", "you"]])
    False
    """
    lenght_1 = len(image[0])
    for index in range(1, len(image)):
        lenght_2 = len(image[index])
        if lenght_1 != lenght_2:
            return False
        index +=1
    
    for sublist in image:
        for element in sublist:
            if type(element) != type(1):
                return False
    
    i = 0
    for i in range(len(image)):
        for x in range(len(image[i])):
            element = image[i][x]
            if element in range(MAX_WHITE_VALUE+1):
                x += 1
            else:
                return False
        i += 1
    return True
               
def is_valid_compressed_image(compressed_image):
    """ (list<list>) -> bool
    Takes a nested list and returns True if the nested list
    represents a compressed PGM image matrix. Otherwise,
    returns False.
    
    >>> is_valid_compressed_image([["0x5", "200x2"], ["111x7"]])
    True
    
    >>> is_valid_compressed_image([[0, 2], [5, 6], [7, 8]])
    False
    
    >>> is_valid_compressed_image([["258x5", "1x2"], ["1x400"], ["10X5", "0X5"]])
    False
    """
    for sublist in compressed_image:
        for element in sublist:
            if type(element) == type(1):
                return False
            number_x = element.count('x')
            if number_x != 1:
                return False
            
            element_AB = element.split('x')
            for l in element_AB:
                if not l.isdecimal():
                    return False
                #for sub_l in l:
                    #n = 0
                    #while n < len(sub_l):
                        #if sub_l[n] not in DIGIT:
                            #return False
                        #n += 1
    i = 0
    first_sum_of_B = 0
    for i in range(len(compressed_image)):
        sum_of_B = 0
        for x in range(len(compressed_image[i])):
            element = compressed_image[i][x]
            element_AB = element.split('x')
            A = int(element_AB[0])
            B = int(element_AB[1])
            sum_of_B += B
            
            if A not in range (MAX_WHITE_VALUE + 1):
                return False
            x += 1
        if i == 0:
            first_sum_of_B = sum_of_B
        else:
            if sum_of_B != first_sum_of_B:
                return False
        i += 1
    return True
             
def load_regular_image(filename):
    """ (str) -> list<list>
    Takes a filename string  as input and returns it as a regular image matrix (nested list).
    If the resulting image matrix is not valid, raise an AssertionError.
    
    >>> load_regular_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    >>> fobj = open("checkerboard.pgm", "w")
    >>> fobj.write("P2\n5 5\n255\n255 0 255 0 255\n0 255 0 255 0\n255 0 255 0 255\n0 255 0 255 0\n255 0 255 0 255\n")
    87
    >>> fobj.close()
    >>> load_regular_image("checkerboard.pgm")
    [[255, 0, 255, 0, 255], [0, 255, 0, 255, 0], [255, 0, 255, 0, 255], [0, 255, 0, 255, 0], [255, 0, 255, 0, 255]]
    
    >>> fobj = open("invalid2.pgm", "w")
    >>> fobj.write("P2\n1 1\n255\n3 3\n3 3\n")
    19
    >>> fobj.close()
    >>> load_regular_image("invalid2.pgm")
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    fobj = open(filename, "r") 
    file_content = fobj.read()
    list_content = file_content.split('\n')
    conditions = list_content[0:2]
    image_content = list_content[3:-1]
    fobj.close()
    
    final_image_content = []
    for i in image_content:
        sublist = i.split()
        for element in sublist:
            number_x = element.count('x')
            if number_x != 0:
                raise AssertionError("Compressed format detected.")
        sublist = [int(x) for x in sublist]
        final_image_content.append(sublist)
    
    image_size = conditions[1]
    image_size = image_size.split()
    for e in image_size:
        if not e.isdecimal():
            raise AssertionError("Invalid width or height.")
        #for s in e:
            #if s not in DIGIT:
    
    width = image_size[0]
    height = image_size[1]
    
    if len(final_image_content) != int(height) or len(final_image_content[0]) != int(width):
        raise AssertionError("Invalid image matrix.")
    
    if is_valid_image(final_image_content):
        return final_image_content
    else:
        raise AssertionError("Invalid image matrix.")

def load_compressed_image(filename):
    """ (str) -> list<list>
    Takes a filename string as input and returns it as a compressed image matrix (nested list).
    If the resulting image matrix is not valid, raise an AssertionError.
    
    >>> load_compressed_image("comp.pgm.compressed")
    [['0x24'],
    ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'],
    ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'],
    ['0x24']]
    
    >>> fobj = open("valid_test.pgm", "w")
    >>> fobj.write("P2\n4 4\n255\n0x4\n7x4\n7x4\n0x4\n")
    27
    >>> fobj.close()
    >>> load_compressed_image("valid_test.pgm")
    [['0x4'], ['7x4'], ['7x4'], ['0x4']]
    
    >>> fobj = open("invalid_test.pgm", "w")
    >>> fobj.write("P2C\n3 3\n255\nabc1x2 0x1\n77xc3\n0xw1 1x2\n")
    38
    >>> fobj.close()
    >>> load_compressed_image("invalid_test.pgm")
    Traceback (most recent call last):
    AssertionError: A non-decimal input was detected.
    """
    fobj = open(filename, "r") 
    file_content = fobj.read()
    list_content = file_content.split('\n')
    conditions = list_content[0:2]
    image_content = list_content[3:-1]
    fobj.close()
    
    final_image_content = []
    for i in image_content:
        sublist = i.split()
        final_image_content.append(sublist)
        
    image_size = conditions[1]
    image_size = image_size.split()
    for e in image_size:
        for s in e:
            if not e.isdecimal():
                raise AssertionError("Invalid width or height.")
                
    width = int(image_size[0])
    height = int(image_size[1])
    
    for i in range(len(final_image_content)):
        sum_of_B = 0
        for x in range(len(final_image_content[i])):
            element = final_image_content[i][x]
            element_AB = element.split('x')
            for s in element_AB:
                if not s.isdecimal():
                    raise AssertionError("A non-decimal input was detected.")
                #for sub_s in s:
                    #n = 0
                    #while n < len(sub_s):
                        #if sub_s[n] not in DIGIT:
                            
                        #n += 1
                        
            B = int(element_AB[1])
            sum_of_B += B
    
        if sum_of_B != width or len(final_image_content) != height:
            raise AssertionError("Invalid image matrix.")
    
    if is_valid_compressed_image(final_image_content):
        return final_image_content
    else:
        raise AssertionError("Invalid compressed image matrix.")

def load_image(filename):
    """ (str) -> list<list>
    Takes a filename string  as input and returns it as a regular or a compressed
    image matrix (nested list). If it is a regualr image, load regular PGM image.
    If it is compressed image, load compressed image. Otherwise, raises an AssertionError 
    
    >>> load_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]    
    
    >>> fobj = open("aaaa.pgm", "w")
    >>> fobj.write("P2C\n1 4\n255\nax1\nax1\nax1\nax1\n")
    28
    >>> fobj.close()
    >>> load_image("aaaa.pgm")
    Traceback (most recent call last):
    AssertionError: A non-decimal input was detected.
    
    >>> fobj = open("valid_test.pgm", "w")
    >>> fobj.write("P2\n4 4\n255\n0x4\n7x4\n7x4\n0x4\n")
    27
    >>> fobj.close()
    >>> load_image("valid_test.pgm")
    [['0x4'], ['7x4'], ['7x4'], ['0x4']]
    """
    fobj = open(filename, "r")
    file_content = fobj.read(3)
    fobj.close()
    
    if 'P2C' in file_content:
        return load_compressed_image(filename)
    elif 'P2C' not in file_content: 
        return load_regular_image(filename)
    else:
        raise AssertionError("Does not respect the image matrix for neither regular or compressed PGM image.")

def save_regular_image(image, filename):
    """ (list<list>, str) -> NoneType
    Takes a nested list and a filename (string) as input, and saves it in the PGM
    format to a file with the given filename.
    If it is a regular image, save regular image. Otherwise, raise an AssertionError
    
    >>> save_regular_image([[0]*10, [255]*10, [0]*10], "test.pgm")
    >>> fobj = open("test.pgm", 'r')
    >>> fobj.read()
    'P2\n10 3\n255\n0 0 0 0 0 0 0 0 0 0\n255 255 255 255 255 255 255 255 255 255\n0 0 0
    0 0 0 0 0 0 0\\n'
    >>> fobj.close()
    >>> image = [[0]*10, [255]*10, [0]*10]
    >>> save_regular_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    
    >>> save_regular_image([["abc"], [255]*10, [0]*10], "test.pgm")
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    
    >>> save_regular_image([[0]*7, [255]*10, [0]*10], "test.pgm")
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    if is_valid_image(image):
        width = str(len(image[0]))
        height = str(len(image))
        fobj = open(filename, "w")
        filename = fobj.write("P2\n")
        filename = fobj.write(width)
        filename = fobj.write(" ")
        filename = fobj.write(height+"\n")
        filename = fobj.write(str(MAX_WHITE_VALUE))
        
        for sublist in image:
            filename = fobj.write("\n")
            i = 0
            for element in sublist:
                x = str(element)
                if i < len(image[0])-1:
                    filename = fobj.write(x)
                    filename = fobj.write(' ')
                    i += 1
                else:
                    filename = fobj.write(x)
        filename = fobj.write("\n")
        fobj.close()
    else:
        raise AssertionError("Invalid image matrix.")

def save_compressed_image(compressed_image, filename):
    """
    (list<list>, str) -> Type
    Takes a nested list and a filename (string) as input, and saves it in the PGM
    format to a file with the given filename.
    If it is a compressed image, save compressed image. Otherwise, raise an AssertionError.
    
    >>> save_compressed_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    >>> image = [["0x5", "200x2"], ["111x7"]]
    >>> save_compressed_image(image, "test.pgm")
    >>> image2 = load_compressed_image("test.pgm")
    >>> image == image2
    True
    
    >>> save_compressed_image([["0x1", "200x2"], ["111x7"]], "test.pgm.compressed")
    Traceback (most recent call last):
    AssertionError: Invalid compressed image matrix
    
    >>> save_compressed_image([["0x5", "aaax2"], ["111x7"]], "test.pgm.compressed")
    Traceback (most recent call last):
    AssertionError: Invalid compressed image matrix
    """
    if is_valid_compressed_image(compressed_image):
        w = 0
        for x in range(len(compressed_image[0])):
            element = compressed_image[0][x]
            element_AB = element.split('x')
            w += int(element_AB[1])
            
        width = str(w)
        height = str(len(compressed_image))
        
        fobj = open(filename, "w")
        filename = fobj.write("P2C\n")
        filename = fobj.write(width)
        filename = fobj.write(" ")
        filename = fobj.write(height)
        filename = fobj.write("\n")
        filename = fobj.write(str(MAX_WHITE_VALUE))
        for sublist in compressed_image:
            filename = fobj.write("\n")
            i = 0
            for element in sublist:
                last_element = len(sublist)-1
                if i == last_element:
                    filename = fobj.write(element)
                else:
                    filename = fobj.write(element)
                    filename = fobj.write(' ')
                    i += 1
        filename = fobj.write('\n')
        fobj.close()
    else:
        raise AssertionError("Invalid compressed image matrix.")

def save_image(image, filename):
    """
    (list<list>, str) -> NoneType
    Takes a nested list and a filename (string) as input. Checks the type of elements in the
    list to check whether it's a regular image or a compressed image. If valid, save image. Otherwise, raise AssertionError.
    
    >>> save_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    >>> image = [["0x5", "200x2"], ["111x7"]]
    >>> save_image(image, "test.pgm")
    >>> image2 = load_image("test.pgm")
    >>> image == image2
    True
    
    >>> save_image([["abc"], [255]*10, [0]*10], "test.pgm")
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    
    >>> save_image([["0x5", "aaax2"], ["111x7"]], "hehe.pgm.compressed")
    >>> Traceback (most recent call last):
    >>> AssertionError: Invalid compressed image matrix
    """
    if is_valid_image(image):
        save_regular_image(image, filename)
    elif is_valid_compressed_image(image):
        save_compressed_image(image, filename)
    else:
        raise AssertionError("Invalid image matrix.")
    
def invert(image):
    """
    (list<list>) -> list<list>
    Takes a (non-compressed) PGM image matrix as input, and returns the inverted image.
    Should not modify the input matrix. If it is valid image, invert image. Otherwise, raise AssertionError.
    
    >>> image = [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    >>> invert(image)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    >>> image == [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    True
    
    >>> image = [[0, 100, 0], [200, 200, 200], [100, 100, 100]]
    >>> invert(image)
    [[255, 155, 255], [55, 55, 55], [155, 155, 155]]
    >>> image == [[0, 100, 0], [200, 200, 200], [100, 100, 100]]
    True
    
    >>> image = [[0, '7x3', 0], [200, 200, 200], [100, 100, 100]]
    >>> invert(image)
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    if is_valid_image(image):
        final_invert = []
        for i in range(len(image)):
            inv_image = []
            for e in range(len(image[0])):
                inverted_element = 255 - image[i][e]
                inv_image.append(inverted_element)
                e += 1   
            i += 1
            final_invert.append(inv_image)
        return final_invert
    else:
        raise AssertionError("Invalid image matrix.")

def flip_horizontal(image):
    """
    (list<list>) -> list<list>
    Takes a (non-compressed) PGM image matrix as input, and returns the image
    matrix flipped horizontally. Should not modify the input matrix.If it is valid image, flip image.
    Otherwise, raise AssertionError.
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    [[5, 4, 3, 2, 1], [10, 10, 5, 0, 0], [5, 5, 5, 5, 5]]
    
    >>> image = [[5, 4, 3, 2, 1], [0, 0, 5, 11, 9], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    [[1, 2, 3, 4, 5], [9, 11, 5, 0, 0], [5, 5, 5, 5, 5]]
    
    >>> image = [[5, 4, 3, 2, 1], [0, 0, 5, 11, 9], ['5x5']]
    >>> flip_horizontal(image)
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    if is_valid_image(image):
        horizontal_image = []
        for sublist in image:
            horizontal_image.append(sublist[::-1])
        return horizontal_image
    else:
        raise AssertionError("""Invalid image matrix.""")
    
def flip_vertical(image):
    """
    (list<list>) -> list<list>
    Takes a (non-compressed) PGM image matrix as input, and returns the image
    matrix vertically. Should not modify the input matrix.If it is valid image, flip image.
    Otherwise, raise AssertionError.
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [0, 0, 5, 10, 10], [1, 2, 3, 4, 5]]
    
    >>> image = [[5, 4, 3, 2, 1], [0, 0, 5, 11, 9], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [0, 0, 5, 11, 9], [5, 4, 3, 2, 1]]
    
    >>> image = [[5, 4, 3, 2, 1], [0, 0, 5, 11, 9], ['5x5']]
    >>> flip_vertical(image)
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    if is_valid_image(image):
        vertical_image = image[::-1]
        return vertical_image
    else:
        raise AssertionError("""Inavlid image matrix.""")

def crop(image, t_row, t_column, row, column):
    """
    (list<list>, int, int, int, int) -> list<list>
    Takes a (non-compressed) PGM image matrix, two non-negative integers and two positive integers as input.
    Return an image matrix corresponding to the pixels contained in the target rectangle. Should not modify the input list.
    If image is valid, crop image. Otherwise, raise AssertionError.
    
    >>> image = [[5, 5, 5], [5, 6, 6], [6, 6, 7]]
    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2)
    [[6, 6], [6, 7]]
    >>> image == [[5, 5, 5], [5, 6, 6], [6, 6, 7]]
    True
    
    >>> image = [[1, 0, 3, 4], [4, 5, 6, 5], [8, 9, 10, 1]]
    >>> crop([[1, 0, 3, 4], [4, 5, 6, 5], [8, 9, 1, 1]], 1, 2, 2, 1)
    [[6], [1]]
    >>> image == [[1, 0, 3, 4], [4, 5, 6, 5], [8, 9, 10, 1]]
    True
    
    >>> image = [[1, 0, 3, 4], [4, 5, 6, 5], [8, 9, 10, 1]]
    >>> crop([[1, 0, 3, 4], [4, 5, 6, 5], [8, 9, 1, 1]], 1, 3, 2, 2)
    Traceback (most recent call last):
    AssertionError: Out of image
    """
    if is_valid_image(image):
        height = len(image)
        width = len(image[0])
        cropped_image = []
        if t_row not in range(height) or t_column not in range(width):
            raise AssertionError("Starting row or column is out of image.")
        
        if row == 0 and column == 0:
            raise AssertionError("Nothing is cropped.")
        
        if t_column + column not in range(width+1) or t_row + row not in range(height+1):
            raise AssertionError("Out of image")
        
        for i in range(0, row):
            sub_cropped_image = []
            for n in range(0, column):
                sub_cropped_image.append(image[t_row+i][t_column+n])
            cropped_image.append(sub_cropped_image)
        return cropped_image
    else:
        raise AssertionError("""Invalid image matrix.""")
    
def find_end_of_repetition(lst, index, target):
    """
    (list, int, int) -> int
    Takes a list of integers and two non-negative integers (an index and a
    target number) as input. Looks through the list starting after the given index, and returns the index of the last
    consecutive occurrence of the target number.
    
    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 2, 5)
    4
    
    >>> find_end_of_repetition([5, 3, 5, 4, 5, 9, 1], -1, 1)
    6
    
    >>> find_end_of_repetition([5, 3, 5, 4, 5, 9, 1], 1, 1)
    Traceback (most recent call last):
    AssertionError: No target at indicated index.
    """
    if index < 0:
        index = len(lst) + index
    
    if lst[index] != target:
        raise AssertionError("No target at indicated index.")
        
    new_list = lst[index+1:]
    for i in range(len(new_list)):
        if new_list[i] == target:
            index += 1
        elif new_list[i] != target:
            break
    return index

def compress(image):
    """
    list<list> -> list<list>
    Takes a (non-compressed) PGM image matrix as input. If image is valid, compress image.
    Otherwise, raise AssertionError.
    
    >>> compress([[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]])
    [['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']]
    
    >>> compress(load_image("comp.pgm"))
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'],
    ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'],
    ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]
    
    >>> compress([[11, 11, 11, 11, 11], [1, 5, 258, 5, 7], [255, 255, 255, 0, 255]])
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    compressed_image = []
    if is_valid_image(image):
        for sublist in image:
            sub_compressed_image = []
            i = 0
            while i < len(sublist):
                last_rep = find_end_of_repetition(sublist, i, sublist[i])
                new_element = ''
                
                new_element += str(sublist[i])+'x'
                repetition = last_rep + 1 - i
                i += repetition
                new_element += str(repetition)
                repetition = 0
                sub_compressed_image.append(new_element)
                
            compressed_image.append(sub_compressed_image)
        return compressed_image
    else:
        raise AssertionError("""Invalid image matrix.""")

def decompress(compressed_image):
    """
    list<list> -> list<list>
    Takes a compressed PGM image matrix as input. If image is valid, decompress image.
    Otherwise, raise AssertionError.
    
    >>> decompress([['11x5'], ['1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']])
    [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> image = [[11, 11, 11, 11, 11], [1, 5, 5, 5, 7], [255, 255, 255, 0, 255]]
    >>> compressed_image = compress(image)
    >>> image2 = decompress(compressed_image)
    >>> image == image2
    True
    
    >>> decompress(load_image("comp.pgm.compressed"))
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0],
    [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> image = decompress(load_image("comp.pgm.compressed"))
    >>> compressed_image = compress(image)
    >>> image2 = decompress(compressed_image)
    >>> image == image2
    True
    
    >>> decompress([['hi11x5'], ['dude1x1', '5x3', '7x1'], ['255x3', '0x1', '255x1']])
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    """
    image = []
    if is_valid_compressed_image(compressed_image):
        for sublist in compressed_image:
            sub_image = []
            for element in sublist:
                element_AB = element.split('x')
                A = int(element_AB[0])
                B = int(element_AB[1])
                for i in range(B):
                    sub_image.append(A)
            image.append(sub_image)
        return image   
    else:
        raise AssertionError("""Invalid image matrix.""")
    
def process_command(command):
    """
    (str) -> NoneType
    Takes a string as input corresponding to a series of space-separated
    image processing commands, and executes each command in turn. Does not return anything.
    
    >>> process_command("LOAD<comp.pgm> CP DC INV INV SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True
    
    >>> process_command("LOAD<comp.pgm> CP DC FH FH SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True
    
    >>> process_command("LOAD<comp.pgm> CP DC INT INV SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: One or many of the inputs is not a valid command.
    
    >>> process_command("LOAD<comppgm> CP DC INT INV SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: Invalid filename format.
    
    >>> process_command("LOAD<comp.pgm> CR<1,1,0,h> SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: An non-decimal crop input is detected.
    """
    new_command = command.replace('>', '')
    new_command_1 = new_command.replace('<', ' ')
    list_command = new_command_1.split(' ')
    
    if list_command[0].upper() != 'LOAD' or list_command[-2].upper() != 'SAVE':
        raise AssertionError("The command format is invalid.")
    
    dot_count_1 = list_command[1].count('.')
    dot_count_2 = list_command[-1].count('.')
    if dot_count_1 == 0 or dot_count_2 == 0:
        raise AssertionError("Invalid filename format.")
    
    og_list = list_command[1].split('.')
    final_list = list_command[-1].split('.')
    if len(og_list[0]) <= 0 or len(final_list[0]) <= 0:
        raise AssertionError("Missing filename.")
    
    if 'pgm' not in og_list[1:] or 'pgm' not in final_list[1:]:
        raise AssertionError("Invalid filename.")
    
    previous_command = ''
    for i in range(len(list_command)):
        current_command = list_command[i].upper()
        if current_command == 'LOAD':
            matrix = load_image(list_command[1])
        elif current_command == 'SAVE':
            save_image(matrix, list_command[-1])
            
        elif current_command == 'INV':
            matrix = invert(matrix)
            
        elif current_command == 'FH':
            matrix = flip_horizontal(matrix)
            
        elif current_command == 'FV':
            matrix = flip_vertical(matrix)
            
        elif current_command == 'CR':
            position = list_command[i+1].split(',')
            
            for element in position:
                if not element.isdecimal():
                    raise AssertionError("An non-decimal crop input is detected.")
                
            if len(position) != 4:
                raise AssertionError("Missing input for crop.")
            
            y = int(position[0])
            x = int(position[1])
            h = int(position[2])
            w = int(position[3])
            matrix = crop(matrix, y,x,h,w)
            
        elif current_command == 'CP':
            matrix = compress(matrix)
            
        elif current_command == 'DC':
            matrix = decompress(matrix)
        
        elif previous_command == 'CR' or previous_command == 'LOAD' or previous_command == "SAVE":
            continue
        
        else:
            raise AssertionError("One or many of the inputs is not a valid command.")
        
        previous_command = current_command

 

    
    
    
    


    
    
    
    
    
