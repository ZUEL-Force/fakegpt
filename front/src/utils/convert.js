import showdown from "showdown";

const convert=new showdown.Converter()
convert.setFlavor('github');
convert.setOption("tables",true)
convert.setOption("emoji",true)
convert.setOption("smoothLivePreview",true)
convert.setOption("parseImgDimensions",true)
function getHTMLByMd(md){
     return convert.makeHtml(md)

}

export {getHTMLByMd}
