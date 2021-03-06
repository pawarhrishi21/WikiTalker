from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from collections import Counter
import os
import pickle
import nltk.data
import errno
from nltk.corpus import stopwords
from shutil import copyfile
from nltk.tag import pos_tag

nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')


def count_time(start):
    """
    :param start:
    :return: return the time in seconds
    """
    import time
    end = time.time()
    return end-start


def search_all_specific_nodes_in_xml_known_node_path(file, node_path):
    # Element.findall() finds only elements with a tag which are direct children of the current element.
    import xml.etree.ElementTree as etree
    tree = etree.parse(file)
    root = tree.getroot()
    for node in root.findall(node_path):
        yield node.text


def read_two_columns_file_to_build_dictionary(file):
    """
    file:
        en-000000001    Food waste or food loss is food that is discarded or lost uneaten.

    Output:
        {'en-000000001': 'Food waste or food loss is food that is discarded or lost uneaten.'}
    """
    d = {}
    with open(file) as f:
        for line in f:
            (key, val) = line.rstrip('\n').split("\t")
            d[key] = val
    return d


def read_two_columns_file_to_build_dictionary_type_specified(file, key_type, value_type):
    d = {}
    with open(file, encoding='utf-8') as f:
        for line in f:
            (key, val) = line.rstrip('\n').split("\t")
            d[key_type(key)] = value_type(val)
        return d


def read_file_line_yielder(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.rstrip('\n')


def read_pickle(pickle_path):
    import pickle
    with open(pickle_path, 'rb') as fp:
        result = pickle.load(fp)
    return result


def read_valid_vocabulary(file_path):
    result = []
    with open(file_path,encoding="utf8") as f:
        for line in f:
            line_element = line.rstrip('\n')
            result.append(line_element)
    return result


def write_simple_list(file, list_to_write):
    with open(file, 'w') as f:
        for item in list_to_write:
            f.write(item + '\n')


def write_list_of_tuple(file, list_to_write):
    with open(file, 'w') as f:
        for item in list_to_write:
            f.write("%s\n" % ('\t'.join(str(item_of_item) for item_of_item in item)))


def write_to_pickle(object_to_write, pickle_path):
    import pickle
    with open(pickle_path, 'wb') as fp:
        pickle.dump(object_to_write, fp, protocol=pickle.HIGHEST_PROTOCOL)


def write_dict_type_specified(file_path, dictionary, key_type):
    with open(file_path, 'w') as f:
        if key_type is 'str':
            for key, value in dictionary.items():
                f.write('%s\t%s\n' % (str(key), str(value)))
        elif key_type is 'int':
            for key, value in dictionary.items():
                f.write('%s\t%s\n' % (int(key), float(value)))
        elif key_type is 'tuple':
            for key, value in dictionary.items():
                key_str = '\t'.join(map(str, key))
                f.write('%s\t%s\n' % (key_str, value))


def write_dict(file_path, dictionary):
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in dictionary.items():
            f.write('%s\t%s\n' % (key, value))


def get_files_startswith(data_folder, starting):
    # Reason to add the third condition to verify files' names are not equal to 'word_count_all.txt': In case before
    # executing the code, dicts_and_encoded_texts_folder folder already has 'word_count_all.txt' file, this function
    # considers the previous word_count_all file as a normal local dict file.
    files = [os.path.join(data_folder, name) for name in os.listdir(data_folder)
             if (os.path.isfile(os.path.join(data_folder, name))
                 and name.startswith(starting)
                 and (name != 'word_count_all.txt'))]
    return files

def mkdir_p(path):
    """Create directory and all its parents if they do not exist
    This is the equivalent of Unix 'mkdir -p path'
    Parameter
    ---------
    path : str
        Path to new directory.
    Reference
    ---------
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise exc

def input(input_folder,output_folder,k,processed_folder,dicts_folder,edges_folder,graph_folder):

    A = sorted(os.listdir(input_folder))
    n = len(A)

    if n == 0:
        print('No input data found')
        return 0

    if n <= k:
        m = 1
        count = n
    else:
        m = n//k
        d = n - m*k
        count = k

    if os.path.isdir(output_folder):
        print(output_folder + ' already exists, using old run\'s input files')

        for i in range(count):
            curr_dir = os.path.join(output_folder,'run_' + str(i+1))
            d = os.path.join(curr_dir,dicts_folder)
            if(os.path.isdir(d)):
                os.system('rm -r ' + d)
                os.mkdir(d)

            e = os.path.join(curr_dir,edges_folder)
            if(os.path.isdir(d)):
                os.system('rm -r ' + e)
                os.mkdir(e)

            g = os.path.join(curr_dir,graph_folder)
            if(os.path.isdir(g)):
                os.system('rm -r ' + g)
                os.mkdir(g)

        return len(os.listdir(output_folder))

    os.mkdir(output_folder)    

    for i in range(count):
        os.mkdir(os.path.join(output_folder,'run_' + str(i+1)))
        curr_dir = os.path.join(output_folder,'run_' + str(i+1))

        os.mkdir(os.path.join(curr_dir,processed_folder))
        os.mkdir(os.path.join(curr_dir,dicts_folder))
        os.mkdir(os.path.join(curr_dir,edges_folder))
        os.mkdir(os.path.join(curr_dir,graph_folder))

        curr = os.path.join(output_folder,'run_' + str(i+1))
        curr = os.path.join(curr,'input')
        os.mkdir(curr)
        if i < d:
            end = min(n,i*m+m+1)
        else:
            end = min(n,i*m+m)
        for j in range(i*m,end):
            copyfile(os.path.join(input_folder,A[j]),os.path.join(curr,A[j]))
            # os.system('cp "' + os.path.join(input_folder,A[j]) + '" "' + curr + '"')       

    return count


def preProcessing(input_raw_data_dir_name, processed_data_dir_name):
    # for suffix stripping
    # ps = PorterStemmer()

    stop_words = set(stopwords.words('english')) 
    
    # to get only english alphabets
    tokenizer = RegexpTokenizer(r'[a-zA-Z.]+')

    # Check if output directory exists
    if os.path.isdir(processed_data_dir_name) is False:
        # Creating ouput directory
        os.mkdir(processed_data_dir_name)

    files = os.listdir(input_raw_data_dir_name)
    for file_name in files:
        # print('reading ', file_name)
        output_file = os.path.join(processed_data_dir_name, file_name)
        file_name = os.path.join(input_raw_data_dir_name, file_name)
        f_out = open(output_file,'w',encoding="utf8")
        with open(file_name,encoding="utf8") as f:
            for i in f:
                line = tokenizer.tokenize(i)
                if line != []:
                    line_ = []
                    for j in range(len(line)):
                        # x = line[j].lower()
                        x = line[j]
                        if x not in stop_words:
                            line_.append(x)
                    line_ = ' '.join(line_)
                    line_ += ' '
            
                    L = line_.split('.')
                    P = ''
                    for l in L:
                        if len(l) > 0:
                            tagged_sent = pos_tag(l.split())
                            propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
                            S = l.split(' ')
                            for s in S:
                                if s in propernouns:
                                    P += s
                                else:
                                    P += 'zzz'
                                P += ' '
                    f_out.write(P)
        f_out.close()
