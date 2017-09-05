from __future__ import print_function
import sys
import itertools as it
import requests as r
import json
import random


def cartesian_product_iter(suffix, shuffled=True, **lists):
    ll = lists.values()
    k = lists.keys()
    prod = list(it.product(*ll))

    R = ['&'.join(set(it.imap(lambda x: '='.join([str(i) for i in x]),
                                 it.chain.from_iterable(el))))
            for el in (zip(zip(k,cp),
                           it.repeat((suffix,),len(k)))
                       for cp in prod)]

    if shuffled:
        random.shuffle(R)
    return R


def get_n_diseases(num):
    url = "http://localhost:9200/mkes5_association-data/_search"

    diseases_1k_q = {
        "query": {
            "constant_score": {
                "filter": {
                    "exists": {
                        "field": "target.id"
                    }
                }
            }
        },
        "size": num,
        "_source": ["target.id", "disease.id"]
    }

    headers = {
        'content-type': "application/json",
    }

    response = r.request("GET", url,
                         data=json.dumps(diseases_1k_q),
                         headers=headers)

    results = json.loads(response.text)
    data = [res['_source']['disease']['id'] for res in results['hits']['hits']]
    return data


n_args = len(sys.argv)
host = sys.argv[1] if n_args > 1 else 'http://localhost:8008'


if n_args == 1:
    print('you could pass the host prefix: app <host_prefix> def:',
          host, file=sys.stderr)


protein_levels = range(4)
rna_levels = range(11)
diseases_n = get_n_diseases(10)
facets = ['rna_expression_tissue']
suffix = 'no_cache&size=0'

lines = cartesian_product_iter(suffix, protein_expression_level=protein_levels,
                               rna_expression_level=rna_levels,
                               disease=diseases_n,
                               facets=facets)[0:25]

protein_levels = range(4)
rna_levels = range(11)
diseases_n = get_n_diseases(10)
facets = ['protein_expression_tissue']
suffix = 'no_cache&size=0'

lines += cartesian_product_iter(suffix, protein_expression_level=protein_levels,
                                rna_expression_level=rna_levels,
                                disease=diseases_n,
                                facets=facets)[0:25]

protein_levels = range(4)
rna_levels = range(11)
diseases_n = get_n_diseases(10)
facets = ['protein_expression_level']
suffix = 'no_cache&size=0'

lines += cartesian_product_iter(suffix, protein_expression_level=protein_levels,
                                rna_expression_level=rna_levels,
                                disease=diseases_n,
                                facets=facets)[0:25]

protein_levels = range(4)
rna_levels = range(11)
diseases_n = get_n_diseases(10)
facets = ['rna_expression_level']
suffix = 'no_cache&size=0'

lines += cartesian_product_iter(suffix, protein_expression_level=protein_levels,
                                rna_expression_level=rna_levels,
                                disease=diseases_n,
                                facets=facets)[0:25]

random.shuffle(lines)
for l in lines:
    print(host + '/api/latest/public/association/filter?' + l)

