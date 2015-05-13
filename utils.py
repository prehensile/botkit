import re

def chunk_string( str_in, max_chunk_length ):

    l = len(str_in)
    chunks =[]

    if l <= max_chunk_length:
        chunks = [str_in]
    else:
        spaces = re.finditer( "\s+", str_in )
        start_index = 0
        do_chunking = True
        while do_chunking:
            
            end_index = start_index + max_chunk_length
            
            if end_index > l:
                end_index = l
                do_chunking = False

            if do_chunking:
                # find the chunk of whitespace closest to end_index
                end_space = None
                for space_match in spaces:
                    if space_match.start() > end_index:
                        break
                    if space_match.start() >= start_index:
                        end_space = space_match
                
                if end_space:
                    end_index = end_space.start()

            this_chunk = str_in[start_index:end_index]
            chunks.append( this_chunk )

            start_index = end_index
            if end_space:
                start_index = end_space.end()


    return chunks

# simple test case
if __name__ == '__main__':
    t = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras imperdiet nec erat ac condimentum. Nulla vel rutrum ligula. Sed hendrerit interdum orci a posuere. Vivamus ut velit aliquet, mollis purus eget, iaculis nisl. Proin posuere malesuada ante. Proin auctor orci eros, ac molestie lorem dictum nec. Vestibulum sit amet erat est. Morbi luctus sed elit ac luctus. Proin blandit, enim vitae egestas posuere, neque elit ultricies dui, vel mattis nibh enim ac lorem. Maecenas molestie nisl sit amet velit dictum lobortis. Aliquam erat volutpat."
    chunks = chunk_string( t, 140 )    
    for chunk in chunks:
        print chunk
        print len(chunk)