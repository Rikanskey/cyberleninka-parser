import pydot
from PIL import Image
from io import BytesIO
from mindmapcreator import MindMapCreator


class MindMapWindow:
    def __init__(self):
        self.__map_creator = MindMapCreator()

    def draw_map(self, article_link):
        result_map = self.__map_creator.create_mind_map(article_link)
        graph = pydot.Dot(graph_type='graph', rankdir='UD')
        if len(result_map):
            for key in result_map.keys():
                parent_node = pydot.Node(key)
                for value in result_map[key]:
                    node = pydot.Node(value)
                    graph.add_edge(pydot.Edge(parent_node, node))
            Image.open(BytesIO(graph.create(format='png'))).show()
            return True
        else:
            return False


if __name__ == '__main__':
    m = MindMapWindow()
    m.draw_map('https://cyberleninka.ru/article/n/algoritm-raspoznavaniya-obektov-1')
