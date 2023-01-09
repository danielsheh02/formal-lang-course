grammar GQL;
prog: (LINE_BR? stmt ';' LINE_BR?)+ EOF;

stmt: var '=' expr | 'print' LPAREN expr RPAREN;
var : ID;

expr:
    var
  | val
  | map
  | filter
  | intersection
  | concat
  | union
  | star
  | vertex
  | vertices
  | edge
  | edges
  | label
  | labels
  | bool_expr
  | graph;

val : bool | INT | STR;
bool: 'true' | 'false' ;
map: MAP LPAREN lambda COMMA expr RPAREN;
filter: FILTER LPAREN lambda COMMA expr RPAREN;
intersection: INTERSECT LPAREN expr COMMA expr RPAREN;
concat: CONCAT LPAREN expr COMMA expr RPAREN;
union: UNION LPAREN expr COMMA expr RPAREN;
star: STAR LPAREN expr RPAREN;

bool_expr:
        LPAREN vertex ('NOT')? 'IN' vertices RPAREN;

lambda: 'lambda' ((var COMMA)* (var)?) COLON expr;

graph:
      var
    | ADD_START LPAREN vertices COMMA graph RPAREN
    | ADD_FINAL LPAREN vertices COMMA graph RPAREN
    | SET_START LPAREN vertices COMMA graph RPAREN
    | SET_FINAL LPAREN vertices COMMA graph RPAREN
    | LOAD_GRAPH LPAREN STR RPAREN;

vertex: var | INT;

vertices:
      GET_START LPAREN graph RPAREN
    | GET_FINAL LPAREN graph RPAREN
    | GET_VERTICES LPAREN graph RPAREN
    | GET_REACHABLE LPAREN graph RPAREN
    | LBRACE (vertex COMMA)* (vertex)? RBRACE;

edge: var | LPAREN INT COMMA label COMMA INT RPAREN;

edges:
      GET_EDGES LPAREN graph RPAREN
    | LBRACE (edge COMMA)* (edge)? RBRACE;

label: var | val;

labels:
      GET_LABELS LPAREN graph RPAREN
    | LBRACE (label COMMA)* (label)? RBRACE;

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
COMMA: ',';
COLON: ':';

MAP: 'map' ;
FILTER: 'filter' ;
INTERSECT: 'intersect';
CONCAT: 'concat';
STAR: 'star';
UNION: 'union';

GET_LABELS: 'get_labels';
GET_EDGES: 'get_edges';

ADD_START: 'add_start';
ADD_FINAL: 'add_final';
SET_START: 'set_start';
SET_FINAL: 'set_final';
LOAD_GRAPH: 'load_graph';

GET_START: 'get_start';
GET_FINAL: 'get_final';
GET_REACHABLE: 'get_reachable';
GET_VERTICES: 'get_vertices';

INT: '-'? [1-9] [0-9]* | '0';
STR: '"' .*? '"' ;
ID: [_a-zA-Z][_a-zA-Z0-9]* ;

LINE_BR: [\n]+;
WS : [ \t\r]+ -> skip;
