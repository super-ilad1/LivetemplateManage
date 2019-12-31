# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import os


class livetemplate():
    def __init__(self):
        self.newFileName = ''
        pass

    # 新建一个group
    # <editor-fold desc="基于XML文件的操作">
    def newfile(self, templateName):
        self.newFileName = templateName
        self.root = ET.Element("templateSet", group=self.newFileName)
        pass

    def save(self, location=r'C:\Users\肖洪才\.PyCharm2019.2\config\templates'):

        tree = ET.ElementTree(self.root)
        tree.write(location + '\\' + self.newFileName + '.xml')
        pass

    # 读取单个template

    def read(self, file, location=r"C:\Users\肖洪才\.PyCharm2019.2\config\templates", test=False):
        if test:
            pass
        else:
            location = location + '\\' + file + '.xml'
            # print("location: "+location)

        self.tree = ET.parse(location)
        root = self.tree.getroot()

        # print(root.tag) #templateSet
        # print(root) #<Element 'templateSet' at 0x02FE9930>

        # for i in root:
        #     print(i.tag,i.attrib) #template {'description': 'assume this is the desc', 'name': 'panda_export_mysql', 'toReformat': 'false', 'toShortenFQNames': 'true', 'value': 'assume this is the content'}

        # 第一个template，第二个context，第三个option
        # print(root[0][0][0].attrib) #{'name': 'Python', 'value': 'true'}
        dict = []
        # 给环境的list

        count = 0
        # note 处理读取文件
        for template in root.iter('template'):
            envilist = []
            variablelist = []
            count += 1

            # 读取variable
            try:
                for variableElement in template.findall('variable'):
                    print(variableElement.get('name'))
                    variablelist.append(variableElement.get('name'))

            except Exception as e:
                print(e)
                pass

            for contextElement in template.find('context'):
                envilist.append(contextElement.get('name'))

            if len(envilist) == 0:
                envilist = []

            value = template.attrib['value']
            # print(value)
            name = template.attrib['name']
            # print(name)
            desc = template.attrib['description']
            # print(desc)
            # print(template.option.attrib['name'])
            dict.append({'id': count, 'envi': envilist, 'value': value, 'desc': desc, "name": name, 'status': False,
                         'variables': variablelist})

        print(dict)
        '''{'name': 'tkinter_combobox', 'value': "box=Combobox(window)\nbox['values']=(1,2,3,4,'box')\nbox.current(1)\nbox.pack()", 'description': '', 'toReformat': 'false', 'toShortenFQNames': 'true'}
                {'name': 'tkinter_checkbutton', 'value': "chk_state = BooleanVar()\nchk_state.set(True)  # set check state\nchk = Checkbutton(window, text='Choose', var=chk_state)", 'description': '', 'toReformat': 'false', 'toShortenFQNames': 'true'}
                '''
        return dict

        pass

        # "C:\Users\肖洪才\Documents\OneNoteGem\test.xml"

    # 读取Template下的文件
    def readAllFile(self):
        fileList = [i[:-4] for i in os.listdir(r'C:\Users\肖洪才\.PyCharm2019.2\config\templates')]
        return fileList

    # </editor-fold>

    # <editor-fold desc="文件的增删查改">
    # <editor-fold desc="Notes">
    # name eg:panda_export_mysql
    # value eg:set_option('display.max_rows',5)&#10;set_option('di........
    # description eg:读取文件
    # apply:python
    # </editor-fold>
    def addTemplate(self, root,unit):
        # name, value, desc, enviList, variableList
        name = unit['name']
        value = unit['value']
        desc = unit['desc']
        print("this is desc from update(): ",desc)
        print("this is unit from update(): ",unit)
        enviList = unit['envi']

        variableList = unit['variables']
        # print('variableList',variableList)

        template = ET.SubElement(root, "template", name=name, value=value, description=desc, toReformat="false",
                                 toShortenFQNames="true")
        if len(variableList) > 0:

            for i in variableList:
                ET.SubElement(template, "variable", name=i, expression="", defaultValue="", alwaysStopAt="true")

        context = ET.SubElement(template, "context")

        if len(enviList) > 0:
            for i in enviList:
                ET.SubElement(context, "option", name=i, value="true")

        pass

    # </editor-fold>
    # note update()更新
    def update(self,updatedinfos, title):
        location=r"C:\Users\肖洪才\.PyCharm2019.2\config\templates"+"\\"+title+".xml"
        self.tree = ET.parse(location)
        root = self.tree.getroot()

        # count=0
        print(root[0].get('name'))
        for template in root.findall('template'):
            # print(template)
            root.remove(template)

        for templateUnit in updatedinfos:
            # print(templateUnit)
            self.addTemplate(root,templateUnit)

        tree = ET.ElementTree(root)
        tree.write(location)

        # for template in root.findall('template'):


        # root.remove(template)


#         append(subelement)
# Adds the element subelement to the end of this elements internal list of subelements.

# note main执行
if __name__ == '__main__':
    pass

    # <editor-fold desc="新建一个文件测试">
    #     livet = livetemplate()
    #     livet.newfile('test10')
    #     a='''assume this is the content$user$
    # assume this is the content$END$
    #     assume this is the content'''
    #     livet.addTemplate('panda_export_mysql',a, 'assume this is the desc', 'python')
    #
    # livet.save()
    # </editor-fold>

    # <editor-fold desc="读取查询测试">
    # livet = livetemplate()
    # livet.read("", location=r"C:\Users\肖洪才\.PyCharm2019.2\config\templates\Angular.xml", test=True)

# </editor-fold>

# <editor-fold desc="读取Live template文件测试">
# livet = livetemplate()
# livet.readAllFile()

# </editor-fold>


    # <editor-fold desc="更新infos测试">
    testUpdatedInfos=[{'id': 1, 'envi': ['Django', 'HTML_TEXT', 'JAVA_SCRIPT'], 'value': '<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.6.10/vue.common.dev.js"></script>', 'desc': '通过CDN导入Vue.js模板', 'name': 'vue_cdn引入', 'status': True, 'variables': []}, {'id': 2, 'envi': ['Django', 'HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.19.0/axios.js"\n            integrity="sha256-XmdRbTre/3RulhYk/cOBUMpYlaAp2Rpo/s556u0OIKk=" crossorigin="anonymous"></script>', 'desc': '引入axios_ajax的cdn模板', 'name': 'axios导入', 'status': False, 'variables': []}, {'id': 3, 'envi': ['Django', 'ECMAScript6', 'HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': 'watch:{\n            msg: function (newOne,oldOne) {\n                if (newOne == "haha") {\n                    this.msg="you input haha!!"\n                }\n\n            }\n\n\n        }', 'desc': 'vue watch template', 'name': 'watch_vue_template', 'status': False, 'variables': []}, {'id': 4, 'envi': ['ECMAScript6', 'ES6_CLASS', 'ES6_EXPRESSION', 'ES6_STATEMENT', 'JAVA_SCRIPT', 'JSX_HTML', 'JS_CLASS', 'JS_EXPRESSION', 'JS_STATEMENT'], 'value': 'data: {\n            //timeSet: "",\n            //list:[]\n        }', 'desc': 'data vue template', 'name': 'data_vue_template', 'status': False, 'variables': []}, {'id': 5, 'envi': ['ECMAScript6', 'ES6_CLASS', 'ES6_EXPRESSION', 'ES6_STATEMENT', 'JAVA_SCRIPT', 'JSX_HTML', 'JS_CLASS', 'JS_EXPRESSION', 'JS_STATEMENT'], 'value': 'directives: {\n            "color": function (el, params) {\n                el.style.color = params.expression;\n\n            }', 'desc': 'vue中如自定义v-color指令模板的使用', 'name': 'directives_vue', 'status': False, 'variables': []}, {'id': 6, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': '//<input ref="input">\n        \n        /*\n\n        methods: {\n          // 用来从父级组件聚焦输入框\n         focus: function () {\n         this.$refs.input.focus()\n         }\n        }\n\n        */', 'desc': '', 'name': 'ref_vue_template_refs快速使用', 'status': False, 'variables': []}, {'id': 7, 'envi': ['Django', 'HTML_TEXT'], 'value': '<script src="https://cdnjs.cloudflare.com/ajax/libs/vue-router/3.1.3/vue-router.min.js"></script>', 'desc': 'vue_router的CDN导入', 'name': 'vue_router_CDN', 'status': False, 'variables': []}, {'id': 8, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': 'v-for="item,i in $list$"', 'desc': '', 'name': 'v-for="item,i in list">', 'status': False, 'variables': ['list']}, {'id': 9, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '\nVue.component(\'button-counter\', {\n        data: function () {\n            return {\n                count: 0\n            }\n        },\n        template: \'<button v-on:click="count++">You clicked me {{ count }} times.</button>\'\n    });\n\n    /*1.必须放在初始化的new Vue({ })之前！！\n    \n    2.html中应该这样子设置\n    <div id="components-demo">\n        <button-counter></button-counter>\n    </div>\n    \n\n3.组件的本质\nvar login={\n\n    template:\'<h1>this is template</h1>\'\n};\n\nVue.components(\'templateName\', login);\n\n*/', 'desc': '共有组件的创建', 'name': 'components_vue_共有组件的创建', 'status': False, 'variables': []}, {'id': 10, 'envi': ['ECMAScript6', 'ES6_CLASS', 'ES6_EXPRESSION', 'ES6_STATEMENT', 'JAVA_SCRIPT', 'JSX_HTML', 'JS_CLASS', 'JS_EXPRESSION', 'JS_STATEMENT'], 'value': 'methods:{\n            $changed$($para$){\n            $content$\n            }\n        }', 'desc': '创建vue的methods函数', 'name': 'methods_vue', 'status': False, 'variables': ['changed', 'para', 'content']}, {'id': 11, 'envi': ['OTHER'], 'value': '<!--   将下面这个引入到<head>中去-->\n<!--        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.2/animate.css"-->\n<!--              integrity="sha256-a2tobsqlbgLsWs7ZVUGgP5IvWZsx8bTNQpzsqCSm5mk=" crossorigin="anonymous"/>-->\n        \n<!--  点击 https://daneden.github.io/animate.css/  选择指定的css样式 -->\n<!--        enter-active-class和leave-active-class定义了开始和离开的动画，而且开始的class必须是animated，v-if控制显示，flag是bool-->\n        <transition name="my" enter-active-class="animated bounceIn" leave-active-class="animated bounceOut">\n            <p v-if="flag">Test</p>\n        </transition>\n        \n        ', 'desc': 'animated.css的使用', 'name': 'animated_vue', 'status': False, 'variables': []}, {'id': 12, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '<!--   将下面这个引入到<head>中去-->\n<!--        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.2/animate.css"-->\n<!--              integrity="sha256-a2tobsqlbgLsWs7ZVUGgP5IvWZsx8bTNQpzsqCSm5mk=" crossorigin="anonymous"/>-->\n        \n<!--  点击 https://daneden.github.io/animate.css/  选择指定的css样式 -->\n<!--        enter-active-class和leave-active-class定义了开始和离开的动画，而且开始的class必须是animated，v-if控制显示，flag是bool-->\n        <transition name="my" enter-active-class="animated bounceIn" leave-active-class="animated bounceOut">\n            <p v-if="flag">Test</p>\n        </transition>\n        \n        ', 'desc': 'animated.css的使用', 'name': '<transition>_animated.css', 'status': False, 'variables': []}, {'id': 13, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '<!--   <style>-->\n<!--   -->\n<!--   -->\n<!--           .my-enter,-->\n<!--           .my-leave-to {-->\n<!--               opacity: 0;-->\n<!--           }-->\n<!--   -->\n<!--   -->\n<!--           .my-enter-active,-->\n<!--           .my-leave-active {-->\n<!--               transition: all 0.8s ease;-->\n<!--           }-->\n<!--       </style>-->\n   \n   \n   \n   <transition name="my">\n       <p v-if="flag">Test</p>\n   </transition>', 'desc': '在vue中定义动画', 'name': '<transition>_vue', 'status': False, 'variables': []}, {'id': 14, 'envi': ['HTML', 'REQUEST'], 'value': '@keyup="$param$"  \n<!--    .enter .right  .left .down .up 快捷键-->', 'desc': 'Vue中的keyup', 'name': '@keyup=""', 'status': False, 'variables': ['param']}, {'id': 15, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '  //  <P>{{ filterTest | process("xiaohaha") }}</P>\n  \n filters: {\n \n            processData:function(data1) {\n                var data = new Date(data1);\n\n                return data.getminutes();\n            }\n        }\n        \n   /*公共\n  \n    Vue.filter("process", function (data, args) {\n        return data.replace(/LALA/g, args)\n\n    });\n    */\n        \n \n', 'desc': 'vue中的私有过滤器使用，eg：{{ msg | process }}', 'name': 'filters:{_vue_eg：{{ msg | process }}', 'status': False, 'variables': []}, {'id': 16, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': '//如何自动执行函数？当页面加载的时候\n created() {\n$pa$\n            console.log("asdas");\n            this.id = this.list.length + 1;\n\n        }', 'desc': '自动加载函数created()函数', 'name': 'created()_vue 自动加载函数', 'status': False, 'variables': ['pa']}, {'id': 17, 'envi': ['ECMAScript6', 'ES6_CLASS', 'ES6_EXPRESSION', 'ES6_STATEMENT', 'JAVA_SCRIPT', 'JSX_HTML', 'JS_CLASS', 'JS_EXPRESSION', 'JS_STATEMENT'], 'value': 'components: {\n            \'compa\': {\n                props: ["parenttag"],\n                template: "#test1",\n                data:function(){\n                    return {\n                        count:0\n                    }\n                }\n                //务必记住 :parenttag后面如果是string,就要双重"\'string\'",默认是变量\n                //props的用法 <compa :parenttag="msg"></comp1>\n                //在template中  <p> {{ parenttag }}\n                //在html中召唤LM,然后输入template就可以弄出template来\n                \n                //  如何使用data中的数据：<button @click="count++">Increment</button>\n                //                      <p>i love you very much {{ count }}</p>\n\n\n            },\n        }', 'desc': '', 'name': 'components_定义私有的Vue对象', 'status': False, 'variables': []}, {'id': 18, 'envi': ['ES6_STATEMENT', 'JS_STATEMENT'], 'value': 'var vm1=new Vue({\n        el:"$a$",\n        data:{\n            $ab$:"$af$"\n        }, \n        methods: {\n            function() {\n            //    do something\n            }\n        }\n    })', 'desc': '', 'name': 'vue Initial 创建一个new Vue对象', 'status': False, 'variables': ['a', 'ab', 'af']}, {'id': 19, 'envi': ['ES6_STATEMENT', 'JS_STATEMENT'], 'value': "axios.post('/timeslider/', {\n                    'id': 'asdas'\n                }).then((data) => {\n                        this.msg = data;\n                        console.log(data);\n\n                        // views中的设置 return JsonResponse({'name': 'OK'})\n                        //传递的参数默认是Json形式\n\n                    }\n                );", 'desc': '', 'name': 'axios_post的函数调用', 'status': False, 'variables': []}, {'id': 20, 'envi': ['CSS', 'HTML'], 'value': 'v-cloak\n\n/*把下面的添加到css中*/\n/*[v-cloak] {*/\n/*    display: none;*/\n\n/*}*/', 'desc': '', 'name': 'v-cloak_vue防止闪烁', 'status': False, 'variables': []}, {'id': 21, 'envi': ['HTML', 'JAVA_SCRIPT', 'REQUEST'], 'value': ' @click.prevent=“”\n//阻止默认事情，比如<a>中的href跳转', 'desc': '', 'name': '@click.prevent_阻止默认事件模板', 'status': False, 'variables': []}, {'id': 22, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': '@click.once=""\n//点击事件只触发一次', 'desc': '', 'name': '@click.once_只触发一次事件模板', 'status': False, 'variables': []}, {'id': 23, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': ' search(keyword) {\n   var Newlist = [];\n   console.log(this.keyword);\n   var newlist = this.list.filter(item => {\n                          if (item.name.includes(this.keyword)) {\n                              return item;\n                          }\n                      });\n                      return newlist;\n\n\n                  }\n\n }', 'desc': '', 'name': 'search_vue中的搜索功能函数', 'status': False, 'variables': []}, {'id': 24, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': '<template id="comp1">\n    <p>\n        <slot></slot>\n    </p>\n</template>\n\n<comp1>this is slot</comp1>\n', 'desc': '', 'name': 'slot_vue中组件的slot使用', 'status': False, 'variables': []}, {'id': 25, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': ':style="{ color: \'red\', \'font-size\': \'120px\' }"\n<!--\n1.记住里面的属性必须加上 \' \'比如font-size变成\'font-size\'\n2.此外还可以变成一个Object\n:style="styleObject"\nstyleObject: {\n    color: \'red\',\n    fontSize: \'13px\'\n  }\n\n3.还可以升级到数组\n:style="[baseStyles, overridingStyles]"\n-->', 'desc': '', 'name': ':style_vue中的动态style使用', 'status': False, 'variables': []}, {'id': 26, 'envi': ['HTML', 'JAVA_SCRIPT'], 'value': ':class="{\'list-group-item\':true, \'list-group-item-action\':true,}"\n<!--\n1.记住属性要加上 \'  \' 号\n2.属性后面跟上bool，以控制开关\n3.你还可以这样子：\n<div v-bind:class="classObject"></div>\n\t\tdata: {\n  classObject: {\n    active: true,\n    \'text-danger\': false\n  }\n}\n4.最后你还可以这样子：\n\t\t<div v-bind:class="[activeClass, errorClass]"></div>\n\t\tdata: {\n  activeClass: \'active\',\n  errorClass: \'text-danger\'\n}\n\t\t渲染为：\n\t\t<div class="active text-danger"></div>\n5.以及这样子：\n\t<div v-bind:class="[{ active: isActive }, errorClass]"></div>\n-->\n\n', 'desc': '', 'name': ':class_vue中的动态class使用', 'status': False, 'variables': []}]


    livet = livetemplate()
    livet.update(testUpdatedInfos,location=r"C:\Users\肖洪才\.PyCharm2019.2\config\templates\test2.xml")

    # </editor-fold>
