import glob
import os
import shutil
import codecs


def file_restore(file_name, file_extension, high_word, low_word, file_size, clusters_num, cluster_size):
    file = '\\\\.\\D:'
    f = open(file, 'rb')

    offset = high_word
    if(offset == 0):
        offset = low_word

    #skip offset bytes, high word or low word
    f.read((offset+134)*cluster_size)

    if(clusters_num <= 1):
        long_file_name = file_name + "." + file_extension
        file_content = f.read(file_size).hex()

        rel_path = "files_recovered/" + long_file_name  # relative path
        if(os.path.exists(rel_path)):
            os.remove(rel_path)
        file_to_export = open((rel_path), "wb")
        file_to_export.write(bytes.fromhex(file_content))
        print(bytes.fromhex(file_content))
        file_to_export.close()

    else:
        print("Unavailable Functionality --> More than one cluster linked to this file")

    f.close()


def file_carving():
    usage = shutil.disk_usage("D:\\")
    print("\nDisk usage:")
    print("Total: " + str(usage[0]) + " bytes")
    print("Used: " + str(usage[1]) + " bytes")
    print("Free: " + str(usage[2]) + " bytes\n\n")

    file = '\\\\.\\D:'
    f = open(file, 'rb')
    cluster_size = 1024
    possible_files = 0


    for i in range(0, usage[0]):

        charhex = f.read(1).hex()

        if(charhex != "e5"):
            f.read(15).hex()    #skip the row
        else:

            filenamehexstr = charhex

            # read File Name
            file_name = ""
            for i in range(0, 7):
                charhex = f.read(1).hex()
                #print(charhex)
                charbyte = bytes.fromhex(charhex)
                #print(charbyte)
                try:
                    ascii_str = charbyte.decode("ASCII")
                    file_name = file_name + ascii_str
                    #print("ASCII STRING CHAR: ", ascii_str)
                except:
                    pass

            # read File Extension
            file_extension = ""
            for i in range(0, 3):
                charhex = f.read(1).hex()
                charbyte = bytes.fromhex(charhex)
                try:
                    ascii_str = charbyte.decode("ASCII")
                    file_extension = file_extension + ascii_str
                except:
                    pass

            #skip 9 byte
            f.read(9).hex()

            # read High Word Starting Cluster
            hw_hex_0 = f.read(1).hex()
            hw_hex_1 = f.read(1).hex()
            high_word = int(hw_hex_1 + hw_hex_0, 16)

            # skip 4 byte
            f.read(4).hex()

            # read Low Word Starting Cluster
            lw_hex_0 = f.read(1).hex()
            lw_hex_1 = f.read(1).hex()
            low_word = int(lw_hex_1 + lw_hex_0, 16)

            # read File Size
            fs_hex_0 = f.read(1).hex()
            fs_hex_1 = f.read(1).hex()
            fs_hex_2 = f.read(1).hex()
            fs_hex_3 = f.read(1).hex()
            file_size = int(fs_hex_3 + fs_hex_2 + fs_hex_1 + fs_hex_0, 16)

            #filters to find the deleted file
            if (file_name and file_extension):
                #if(file_name.isalnum() and file_extension.isalnum()):
                if(file_name.isprintable() and file_extension.isprintable()):
                    if (not (high_word != 0 and low_word != 0)):
                        count = 0
                        for a in file_extension:
                            if (a.isspace()) == True:
                                count += 1
                        if(count == 0):
                            clusters_num = round(file_size/cluster_size, 3)
                            possible_files += 1
                            print(possible_files, " File Name: ", file_name, "   File Extension: ", file_extension,
                                   "    High Word: ", high_word, "    Low Word: ", low_word,
                                   "    File Size: ", file_size, "   Number of Clusters: ", clusters_num)
                            file_restore(file_name, file_extension, high_word, low_word, file_size, clusters_num, cluster_size)

    print("\n\nPossible files: ", possible_files)
    f.close()


if __name__ == '__main__':
    file_carving()