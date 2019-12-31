//note vue编辑处

Vue.use(VueCodemirror, {
    options: {
        lineNumbers: true

    }
});

var vm1 = new Vue({
    el: "#operate",

    data: {
        saveSuccess: false,
        MenuSaveNotice: false,
        ifTitleSearch: false,
        MenuNotice: false,
        modelList: {'name': '', 'value': "", 'desc': "", 'envi': []},
        modelDropdown: false,
        navList: [],
        opt: "",
        flag: "false",
        //current content list you are editing
        contentsList: [],
        //current content title you are in
        title: "",
        //the selection of envi for you to choose
        optionList: ['CSS', 'CUCUMBER_FEATURE_FILE', 'CoffeeScript', 'Django', 'ECMAScript6', 'HAML', 'HTML', 'JAVA_SCRIPT', 'JSON', 'PUPPET_FILE', 'Python', 'REQUEST', 'SHELL_SCRIPT', 'SQL', 'TypeScript', 'XML'],
        //the selection value of you select tag
        selectedOne: "",
        codeEditor: null,
        cmOptions: {
            fullScreen: true
        },
        keyword: ""
    },

    methods: {

        //让save显示出来，以说明发生了改动
        switchMenuSaveNotice(boolParam) {
            this.MenuSaveNotice = boolParam;
        },


        saveModel(type) {
            currentItem = this.contentsList.find((item) => {
                if (item.status === true) {
                    return item
                }
            });

            switch (type) {
                case "Envi":
                    this.modelList['envi'] = currentItem.envi;
                    break;
                case "Desc":
                    this.modelList['desc'] = currentItem.desc;
                    break;
                case "Value":
                    this.modelList['value'] = currentItem.value;
                    break;
                case "Name":
                    this.modelList['name'] = currentItem.name;
                    break;

                case "reset":
                    this.modelList['name'] = "";
                    this.modelList['value'] = "";
                    this.modelList['desc'] = "";
                    this.modelList['envi'] = [];

                    break;

            }
            this.modelDropdown = false;


            this.MenuNotice = Object.values(this.modelList).some((item) => {
                return item.length !== 0;
            });


        },

        searchKeyword() {

            var searchTag = this.ifTitleSearch ? '#title1 a' : '#navMenu ul li';

            var keyword = this.keyword;
            console.log('keyword', keyword);
            if (keyword !== "") {


                $(searchTag).each(function () {
                    var text = $(this).text();
                    // console.log(text);
                    if (text.toLowerCase().includes(keyword)) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                });
            } else {
                $(searchTag).each(function () {
                    $(this).show();
                })
            }


        }

        ,
        //拷贝当前的一份
        copy() {
            //找到当前的内容
            var currentContentenvi;
            var currentContentvalue;
            var currentContentstatus;
            var currentContentvariables;
            var currentContentname;
            var currentContentdesc;
            currentContent = this.contentsList.forEach((item) => {
                if (item.status === true) {
                    currentContentenvi = item.envi;
                    currentContentname = item.name;
                    currentContentvalue = item.value;
                    currentContentstatus = item.status;
                    currentContentvariables = item.variables;
                    currentContentdesc = item.desc;

                }
            });

            this.insert();
            this.contentsList.forEach((item) => {
                if (item.status === true) {
                    item.envi = currentContentenvi;
                    item.value = currentContentvalue;
                    item.status = currentContentstatus;
                    item.variables = currentContentvariables;
                    item.desc = currentContentdesc;

                    if (currentContentname.includes('(copy)')) {
                        item.name = currentContentname;
                    } else {
                        item.name = currentContentname + '(copy)';

                    }

                }
            });
        }
        ,


        fullScreen: function () {
            this.$refs.cma[0].codemirror.setOption('fullScreen', 'true')

        }
        ,
        //如何设置codemirror，比如大小之类
        setCodemirror: function () {
            this.$refs.cma[0].codemirror.setSize('1000', '500');

            console.log("this.$refs.cma.codemirror", this.$refs.cma[0].codemirror);

        }
        ,
        //根据文本解析出variables
        extractVariables(string, id) {

            stringList = string.match(/\$([^$]+)\$/gi);
            if (stringList !== null) {
                stringList = stringList.map((item) => {
                    return item.replace(/\$/g, '');
                });
                stringList = stringList.filter(function (item, pos) {
                    return stringList.indexOf(item) === pos;
                });
                console.log("matched expression:", stringList);

                this.contentsList.forEach((item) => {
                    if (item.id === id) {
                        item.variables = stringList;
                    }
                });
            }


        }
        ,


        onCmInput(newCode, id) {
            this.switchMenuSaveNotice(true);
            this.extractVariables(newCode, id);

            console.log(newCode, id);

        }
        ,

        //save all of you edit
        addCodeContent(ID) {
            console.log("addCodeContent");
            console.log(this.codeEditor);
            var value = '';
            $('#textarea2').val('asdasdas');

            // this.codeEditor.setValue('asfasfas');


        }
        ,

        updateCodeContent(ID) {

            this.codeEditor.on('change', function (cm) {
                this.contentsList.forEach((item) => {
                    if (item.id === ID) {
                        item.value = cm.getValue();
                    }
                });

            });
        }
        ,

        //把当前的contentlist全部发送到后端更新
        save() {

            this.switchMenuSaveNotice(false);
            axios.post('/save/', {
                'updatedinfos': this.contentsList,
                'title': this.title
            }).then((data) => {

                if (data.data === 'Yes') {
                    //save success and pop up alert
                    this.saveSuccess = true;
                    console.log('saveSuccessAction');
                    setTimeout(() => {
                        this.saveSuccess = false;
                    }, 500);

                }


                // views中的设置 return JsonResponse({'name': 'OK'})
                //传递的参数默认是Json形式

            });


        }
        ,

        //cancel envi through envi button
        cancelEnvi(id, enviname) {
            this.switchMenuSaveNotice(true);
            console.log('enviname in id: ', id);
            console.log('the enviname you want cancel: ', enviname);
            this.contentsList.forEach((item) => {
                if (item.id === id) {
                    item.envi.forEach((loopedEnviName, index) => {
                        console.log("index", index);
                        if (loopedEnviName === enviname) {
                            console.log("item.envi before cancel: ", item.envi);
                            item.envi.splice(index, 1);
                            console.log("item.envi after cancel: ", item.envi);


                        }
                    })
                }
            });
        }
        ,
        //add new envi option
        addselect(event, id) {
            this.switchMenuSaveNotice(true);
            var insertedContent = event.target.value;

            this.contentsList.forEach((item) => {
                if (item.id === id) {
                    if (!(item.envi.includes(insertedContent))) {
                        item.envi.push(insertedContent);

                    }
                }
            });

        }
        ,
        //switch the specific live template file
        showContent(id) {


            //设置codemirror的大小，因为mounted()无法加载，所以只能用这种无奈的方法
            setTimeout(() => {
                this.setCodemirror();
            }, 1);

            this.addCodeContent(id);
            this.selectedOne = "";
            console.log('show:', id);
            this.contentsList.forEach((item) => {
                if (item.id != id) {
                    item.status = false;

                } else {
                    item.status = true;
                }
            });
            //note insert函数处理


        }
        ,
        //insert a new unit into current LM file with empty options
        insert() {
            this.switchMenuSaveNotice(true);
            var maxiId = null;
            console.log("insert");
            if (this.contentsList.length !== 0) {
                maxiId = this.contentsList[0].id;
                this.contentsList.forEach((item) => {
                    if (item.id >= maxiId) {
                        maxiId = item.id;
                    }

                });
                maxiId++;
            } else {
                maxiId = 1;
            }

            console.log('maxiId: ', maxiId);
            this.contentsList.push({
                'id': maxiId,
                'envi': this.modelList.envi,
                'name': this.modelList.name,
                'value': this.modelList.value,
                'status': false,
                'variables': [],
                'desc': this.modelList.desc,
            });
            this.showContent(maxiId)
        }
        ,
        //note cancel函数处理
        //cancel current (with 'true' status) option
        cancel() {
            this.switchMenuSaveNotice(true);

            //remainIndex是被删除对象的position
            var remainedIndex = 0;

            this.contentsList.forEach((item, index) => {
                if (item.status === true) {
                    remainedIndex = index;
                    this.contentsList.splice(index, 1);

                }
            });
            console.log('remainedIndex:', remainedIndex);

            if ((remainedIndex) === this.contentsList.length) {
                remainedIndex--;
                this.contentsList.forEach((item, index) => {
                    if (index === remainedIndex) {
                        this.showContent(item.id);

                    }
                });
            } else {
                this.contentsList.forEach((item, index) => {
                    if (index === remainedIndex) {
                        this.showContent(item.id);

                    }
                });

            }

        }
        ,

        //ajax post for a live template file
        ajaxFor(info) {
            if (info.indexOf("%20")) {
                info = info.replace("%20", " ")
            }

            this.title = info.replace("/home/", "").replace("/", "");

            console.log("ajaxFor");
            console.log(info);
//note 导航的ajax请求
            axios.post(info).then((data) => {
                    console.log("return data: ");

                    this.contentsList = data.data.infos;


                    //set first element display, cause it is strange if it is None display
                    this.showContent(1);

                    // views中的设置 return JsonResponse({'name': 'OK'})
                    //传递的参数默认是Json形式

                }
            );
        }
        ,
    },//如何自动执行函数？当页面加载的时候
    created() {

        this.ajaxFor('/home/Angular/');


    }, components: {
        LocalCodemirror: VueCodemirror.codemirror,

    },
});

