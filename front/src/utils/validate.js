function isValidate(res){
    if(res.data.code===0){
        return true
    }
    return false
}

export {isValidate}
