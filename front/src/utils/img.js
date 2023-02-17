function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}
// function getImg
function getImgPath(url){
    console.log(process.env.VUE_APP_API_HOST+'/'+url)
    return process.env.VUE_APP_API_HOST+'/'+url
}
export {getBase64,getImgPath}
