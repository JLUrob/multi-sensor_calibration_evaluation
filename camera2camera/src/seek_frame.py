#To find corresponding to the timestamp

camera1_index = 1
# with open('dataset1_camera1_order.txt',encoding='utf-8') as file:
with open('dataset2_camera1_order.txt',encoding='utf-8') as file:
# with open('dataset3_camera1_order.txt',encoding='utf-8') as file:
     content = file.read()
     content = content.rstrip()
    #  print(content.rstrip())
content = content.rsplit('\n')
content = [eval(i) for i in content]

# with open('../jpg/210250/image1_timestamp.txt', encoding='utf-8') as f1:
with open('../jpg/210552/image1_timestamp.txt', encoding='utf-8') as f1:
# with open('../jpg/230830/C1_timestamp.txt', encoding='utf-8') as f1:
    content1 = f1.read()
    content1 = content1.rstrip()
content1 = content1.rsplit('\n')
content1 = [float(i) for i in content1]
print(len(content1))
# with open('../jpg/210250/image2_timestamp.txt', encoding='utf-8') as f2:
with open('../jpg/210552/image2_timestamp.txt', encoding='utf-8') as f2:
# with open('../jpg/230830/C2_timestamp.txt', encoding='utf-8') as f2:
    content2 = f2.read()
    content2 = content2.rstrip()
content2 = content2.rsplit('\n')
content2 = [float(i) for i in content2]
print(len(content2))

camera2_order = [] 
for index1 in content:
    timesstamp1 = content1[index1]
    print(timesstamp1)
    m = 999999999.0
    index = -1
    for i in range(len(content2)):
        sub = abs(timesstamp1 - content2[i])
        if sub <= m:
            index = i
            m = sub
    print(content2[index])
    camera2_order.append(index)
print(camera2_order)
            

    

   
