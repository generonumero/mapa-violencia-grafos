#!/usr/bin/python
#-*- encoding: utf-8 -*-
# Copyright © 2019 Gênero e Número
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public Lic

import codecs
import datetime
import json
import uuid

from collections import defaultdict
from pprint import pprint

import rows

# Gera IDs únicos para cada 
TYPE_IDS = {
    n: str(uuid.uuid4())
    for n in ('norma', 'grupo', 'tema', 'tipo', 'grupo-norma', 'tema-norma', 'tipo-norma')
}

UFS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG',
        'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO',
        'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

# Configuração de cores do grafo
COLOR_NORMA = u'#000'
COLOR_TIPO = u'#9FB592'
COLOR_GRUPO = u'#85988B'
COLOR_TEMA = u'#B6D36D'
COLOR_EDGE = u'#777777'
COLOR_TIPO_EDGE = u'#9FB592'
COLOR_GRUPO_EDGE = u'#85988B'
COLOR_TEMA_EDGE = u'#B6D36D'


def estruturar_dados(sheet):
    """Recebe uma planilha de dados em formato `rows.Table` e retorna uma estrutura de dados equivalente"""
    normas = {}
    tipos_da_violencia = defaultdict(lambda: [])
    grupos_assistidos = defaultdict(lambda: [])
    temas = defaultdict(lambda: [])

    for row in sheet:
        nome = row.numero
        norma = {
            'uf': row.uf,
            'tipo_da_norma': row.tipo_da_norma,
            'ano': row.ano,
            'resumo': row.resumo,
            'link': row.link,
        }

        normas[nome] = norma


        gs = [g.strip() for g in row.tipo_da_violencia.split(';')]
        for g in gs:
            tipos_da_violencia[g].append(nome)

        gs = [g.strip() for g in row.grupo_assistido.split(';')]
        for g in gs:
            grupos_assistidos[g].append(nome)

        gs = [g.strip() for g in row.tema.split(';')]
        for g in gs:
            temas[g].append(nome)

    return {
        'normas': normas,
        'tipos_da_violencia': dict(tipos_da_violencia),
        'grupos_assistidos': dict(grupos_assistidos),
        'temas': dict(temas),
    }


def generate_graph(dados):
    graph = {
        'id': str(uuid.uuid4()),
        'name': u'GN',
        'subtitle': None,
        'description': None,
        'updated_at': str(datetime.datetime.now()),
        'created_at': str(datetime.datetime.now()),
        'status': 0,
         # Possibilidade de colocar imagem na pré-visualização
        'image': {
         'path': None,
         'ref_name': None,
         'ref_url': None,
        },

        # Nós e arestas serão preenchidos depois
        'nodes': [
        ],
        'edges': [
        ],

        # Lista os tipos de nós: 
        'nodeTypes': [
         {
            'id': TYPE_IDS[u'norma'],
            'name': u'Norma',
            'name_alias': None,
            'description': None,
            'hide_name': None,
            'display_name': None,
            'centered_display_name': None,
            'centered_secondary_display_name': None,
            'secondary_display_name': None,
            'image': None,
            'color': COLOR_NORMA,
            'image_as_icon': False,
            'size': u'neutral',
            'size_limit': 10,
            'properties': [
               {
                  'name':'Link',
                  'name_alias':'Link'
               },
               {
                  'name':'Ano',
                  'name_alias':'Ano'
               },
               {
                  'name':'Tipo da norma',
                  'name_alias':'Tipo da norma'
               },
               {
                  'name':'UF',
                  'name_alias':'UF'
               }
            ],
         },
         {
            'id': TYPE_IDS[u'tipo'],
            'name': u'Tipo da violência',
            'name_alias': None,
            'description': None,
            'image': None,
            'image_as_icon': False,
            'color': COLOR_TIPO,
            'properties': [
            ],
            'hide_name': None,
            'size': u'metric_degree',
            'size_limit': 10
         },
         {
            'id': TYPE_IDS[u'grupo'],
            'name': u'Grupo assistido',
            'name_alias': None,
            'description': None,
            'image': None,
            'image_as_icon': False,
            'color': COLOR_GRUPO,
            'properties': [
            ],
            'hide_name': None,
            'size': u'metric_degree',
            'size_limit': 10
         },
         {
            'id': TYPE_IDS[u'tema'],
            'name': u'Tema',
            'name_alias': None,
            'description': None,
            'image': None,
            'image_as_icon': False,
            'color': COLOR_TEMA,
            'properties': [
            ],
            'hide_name': None,
            'size': u'metric_degree',
            'size_limit': 128
         },
        ],
        'edgeTypes': [
         {
            'id': TYPE_IDS[u'tipo-norma'],
            'name': u'é do tipo',
            'name_alias': None,
            'description': None,
            'weighted': 1,
            'directed': 0,
            'durational': None,
            'color': COLOR_TIPO_EDGE,
            'properties': [
            ]
         },
         {
            'id': TYPE_IDS[u'grupo-norma'],
            'name': u'assiste o grupo',
            'name_alias': None,
            'description': None,
            'weighted': 1,
            'directed': 1,
            'durational': None,
            'color': COLOR_GRUPO_EDGE,
            'properties': [
            ]
         },
         {
            'id': TYPE_IDS[u'tema-norma'],
            'name': u'pertence ao tema',
            'name_alias': None,
            'description': None,
            'weighted': 1,
            'directed': 1,
            'durational': None,
            'color': COLOR_TEMA_EDGE,
            'properties': [
            ]
         },
        ]
    }

    for nome, norma in dados['normas'].items():
        node_norma = {
            'id': str(uuid.uuid4()),
            'type': u'Norma',
            'type_id': TYPE_IDS[u'norma'],
            'name': nome,
            'description': norma['resumo'],
            'image': None,
            'reference': None,
            'properties': {
                'Link': norma['link'],
                'Ano': norma['ano'],
                'Tipo da norma': norma['tipo_da_norma'],
                'UF': norma['uf'],
            },
        }

        norma['node_id'] = node_norma['id']

        graph['nodes'].append(node_norma)

    for tipo_v, normas_associadas in dados['tipos_da_violencia'].items():
        node_tipo_v = {
            'id': str(uuid.uuid4()),
            'type': u'Tipo da violência',
            'type_id': TYPE_IDS[u'tipo'],
            'name': tipo_v,
            'description': '',
            'image': None,
            'reference': None,
            'properties': {
            },
        }

        graph['nodes'].append(node_tipo_v)

        for norma in normas_associadas:
            edge = {
                'to': dados['normas'][norma]['node_id'],
                'from': node_tipo_v['id'],
                'name': u'é do tipo',
                'type_id': TYPE_IDS[u'tipo-norma'],
                'id': str(uuid.uuid4()),
                'weight': 1,
                'directed': 1,
                'properties': {
                },
            }
            graph['edges'].append(edge)

    for grupo_a, normas_associadas in dados['grupos_assistidos'].items():
        node_grupo_a = {
            'id': str(uuid.uuid4()),
            'type': u'Grupo assistido',
            'type_id': TYPE_IDS[u'grupo'],
            'name': grupo_a,
            'description': '',
            'image': None,
            'reference': None,
            'properties': {
            },
        }

        graph['nodes'].append(node_grupo_a)

        for norma in normas_associadas:
            edge = {
                'to': dados['normas'][norma]['node_id'],
                'from': node_grupo_a['id'],
                'name': u'assiste o grupo',
                'type_id': TYPE_IDS[u'grupo-norma'],
                'id': str(uuid.uuid4()),
                'weight': 1,
                'directed': 1,
                'properties': {
                },
            }
            graph['edges'].append(edge)

    for tema_a, normas_associadas in dados['temas'].items():
        node_tema_a = {
            'id': str(uuid.uuid4()),
            'type': u'Tema',
            'type_id': TYPE_IDS[u'tema'],
            'name': tema_a,
            'description': '',
            'image': None,
            'reference': None,
            'properties': {
            },
        }

        graph['nodes'].append(node_tema_a)

        for norma in normas_associadas:
            edge = {
                'to': dados['normas'][norma]['node_id'],
                'from': node_tema_a['id'],
                'name': u'pertence ao tema',
                'type_id': TYPE_IDS[u'tema-norma'],
                'id': str(uuid.uuid4()),
                'weight': 1,
                'directed': 1,
                'properties': {
                },
            }
            graph['edges'].append(edge)


    return { 'graph': graph }


if __name__ == '__main__':
    rows = rows.import_from_xlsx("dados.xlsx")
    filtrado = rows
    dados = estruturar_dados(filtrado)

    arq = open('build/grafo-gc.json', 'w')
    json.dump(generate_graph(dados), arq)
    arq.close()

    for uf in UFS:
        filtrado2 = [r for r in filtrado if r.uf == uf]
        filename = 'build/grafo-gc-' + uf + '.json'
        print(filename)
        arq = open(filename, 'w')
        dados = estruturar_dados(filtrado2)
        json.dump(generate_graph(dados), arq)
        arq.close()
