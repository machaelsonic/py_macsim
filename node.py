#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

## 拓扑节点类,方法
class Node():
    def __init__(self, uid='', dist=5, parent = None):
        self.uid = uid
        self.parent_dist = dist      #与父节点的距离
        self.parent = parent
        self.firstchild = None
        self.brother = None
    
    ## 添加子节点
    def add_child(self, child_uid='', dist=0):
        new_child = Node(uid=child_uid, dist=dist, parent=self)
        if self.firstchild is None:
            self.firstchild = new_child
        else:
            last_child = self.firstchild;
            while last_child.brother is not None:
                last_child = last_child.brother
            last_child.brother = new_child
        return new_child
            
            
    def print_branch(self):
        child = self.firstchild
        if child is not None:
            text = "["+self.uid
            while child is not None:
                text += ' '+child.uid
                child = child.brother
            text += "]"
            print text
            
            child = self.firstchild
            while child is not None:
                child.print_branch()
                child = child.brother
    
    ## 获得一条祖先的chain
    def get_parents_chain(self):
        chain = [self]
        p = self.parent
        while p is not None:
            chain.append(p)
            p = p.parent
        chain.reverse()
        return chain
        
    ## 计算节点间距离
    def get_distance(self, other_node):
        chain1=self.get_parents_chain()
        chain2=other_node.get_parents_chain()
        
        if chain1[0] is not chain2[0]:
            print "node %s and node %s are not in the same root" % (self.uid,  other_node.uid)
            return 0
        else:
            while len(chain1) is not 0 and len(chain2) is not 0:
                if(chain1[0] is chain2[0]):
                    chain1.pop(0)
                    chain2.pop(0)
                else:
                    break
            
            dist = 0
            for node in chain1:
                dist += node.parent_dist
            for node in chain2:
                dist += node.parent_dist
            return dist
        
    ## 给定距离, 获得所有距离小于等于该距离的节点
    def get_coverage(self, dist, caller=None):
        chain = [self]
        parent = self.parent
        if parent is not None and parent is not caller:
            if self.parent_dist <= dist:
                chain += parent.get_coverage(dist=dist-self.parent_dist, caller=self)
        
        child = self.firstchild
        while child is not None:
            if child is not caller:
                if child.parent_dist <= dist:
                    chain += child.get_coverage(dist=dist-child.parent_dist, caller=self)
            child = child.brother

        return chain
    
    # 在当前节点下查找指定uid的节点并将其地址返回
    def find_node_in_branch(self, uid):
        if self.uid is uid:
            return self
        else:
            child = self.firstchild
            while child is not None:
                node = child.find_node_in_branch(uid)
                if node is not None:
                    return node
                else:
                    child = child.brother
            return None
    
    # 提供打印
    def __str__(self):
        return self.uid

## 拓扑类:
class Topo():
    def __init__(self, root_node):
        self.root = root_node
        
    def print_nodes_chain(self, nodes_chain):
        for node in nodes_chain:
            print node, 
        

if __name__=='__main__':
    root = Node('root')
    topo = Topo(root)
    root.add_child('1',dist=1)
    root.add_child('2', dist=1)
    root.add_child('3', dist=1)
    
    node = root.find_node_in_branch('1')
    if node is not None:
        node.add_child('11', dist=1)

    node = root.find_node_in_branch('2')
    if node is not None:
        node.add_child('21', dist=1)
        node.add_child('22', dist=1)
    
    node = root.find_node_in_branch('3')
    if node is not None:
        node.add_child('31', dist=1)
        node.add_child('32', dist=1)
    
    root.print_branch()
    
    node = root.find_node_in_branch('32')
    print 'parent chain:', 
    for item in node.get_parents_chain():
        print item, 
    
    print
    if node is not None:
        print 'distance between root and node32', root.get_distance(node)
    
    coverage = 1
    node = root.find_node_in_branch('2')
    print 'all nodes in coverage radius %d:' % coverage, 
    topo.print_nodes_chain(node.get_coverage(coverage))

    print
    print "Exit"
