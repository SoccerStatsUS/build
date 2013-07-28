import os

# FIXME
p = '/home/chris/www/soccerdata/data/sources'




def load():

    def process_line(line):
        if not line.strip():
            return {}


        fields = line.split(';')
        fields = [e.strip() for e in fields]
        if len(fields) == 2:
            name, author = fields
            url = ''
        else:
            try:
                name, author, url = fields
            except:
                import pdb; pdb.set_trace()

        d = {
                'name': name,
                'author': author,
                'base_url': url,
                }

        if 'www.' in url:
            url2 = url.replace('www.', '')
            d2 = d.copy()
            d2['base_url'] = url2
            return [d, d2]
        else:
            return [d]

    l = []

    for line in open(p):
        l.extend(process_line(line))

    return [e for e in l if e]

