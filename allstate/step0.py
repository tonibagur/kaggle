import psycopg2

db=psycopg2.connect(user='coneptum',password='tumconep2012',database='allstate')
cur=db.cursor()
table='train'
length=12
cur.execute('''
select column_name from information_schema.columns where table_name='%s'
order by ordinal_position'''%(table,))
cols=[c[0] for c in cur.fetchall()]
#print cols

cols_new=[]
for i in range(length):
    for c in cols:
        cols_new.append('t%d.%s %s_%d'%(i+1,c,c,i+1))
for c in cols:
    cols_new.append('ty.%s %s_y'%(c,c,))

from_clause=['%s t1' %(table,),'left outer join %s ty on(t1.customer_ID=ty.customer_ID and ty.record_type=1)'%(table,)]
where_clause=['t1.shopping_pt=1','t1.record_type=0']
for i in range(length-1):
    from_clause.append('left outer join %s t%d on (t1.customer_ID=t%d.customer_ID and t%d.record_type=0 and t%d.shopping_pt=%d)'%(table,i+2,i+2,i+2,i+2,i+2))

#print cols_new
#print from_clause

stmt='''
drop table if exists %s_join;
create table %s_join as 
select %s
from %s
where %s
''' % (table,table,','.join(cols_new),
       '\n'.join(from_clause),
       ' and '.join(where_clause),
      )
print stmt
#cur.execute(stmt)
db.commit()


num_bin_cols=['day','group_size','a','b','c','d','e','f','g']
char_bin_cols=['state']
bin_cols=['homeowner']
print "Tenir en compte columna location si hi han problemes de BIAS!!!!"
stmt2='''
select trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN')),count(*)
from %s_join
group by trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN'))
'''
stmt3='''
select trim(coalesce(%s_%s,'UNKNOWN')),count(*)
from %s_join
group by trim(coalesce(%s_%s,'UNKNOWN'))
'''

vals={}

for c in num_bin_cols:
    stmts=[stmt2%(c,'y',table,c,'y')]
    vals[c]=set([])
    for i in range(length):
        s=stmt2%(c,str(i+1),table,c,str(i+1))
        stmts.append(s)
    for s in stmts:
        cur.execute(s)
        for x in cur.fetchall():
            vals[c]=vals[c]|set([x[0]])
for c in char_bin_cols:
    stmts=[stmt3%(c,'y',table,c,'y')]
    vals[c]=set([])
    for i in range(length):
        s=stmt3%(c,str(i+1),table,c,str(i+1))
        stmts.append(s)
    for s in stmts:
        cur.execute(s)
        for x in cur.fetchall():
            vals[c]=vals[c]|set([x[0]])

print vals

select=['customer_id_1']
for i in range(length):
    for c in num_bin_cols:
        for v in sorted(list(vals[c])):
            select.append('''CASE WHEN trim(coalesce(to_char(%s_%s,'99999'),'UNKNOWN'))='%s' THEN 1 ELSE 0 END %s_%s_%s'''%(c,str(i+1),v,c,str(i+1),v))
    for c in char_bin_cols:
        for v in sorted(list(vals[c])):
            select.append('''CASE WHEN trim(coalesce(%s_%s,'UNKNOWN'))='%s' THEN 1 ELSE 0 END %s_%s_%s'''%(c,str(i+1),v,c,str(i+1),v))
    for c in bin_cols:
        select.append(c+'_'+str(i+1))
stmt4='''
select %s
from %s_join''' %(',\n'.join(select),table)

print stmt4
cur.execute(stmt4)
print [c.name for c in cur.description]



