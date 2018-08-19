from Main import io


def main():
    comment_data = io.load_pickle('commentdata.pickle')
    with open('topicsCSV.csv', 'w') as f:
        for word in comment_data:
            f.write(f'{word},{comment_data[word]}\n')

if __name__ == '__main__':
    main()