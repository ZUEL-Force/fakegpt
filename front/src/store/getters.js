const getters={
    isMobile: state => state.app.isMobile,
    theme: state => state.app.theme,
    color: state => state.app.color,
    layout:state=> state.app.layout,
    token: state => state.user.token,
    avatar: state => state.user.avatar,
    nickname: state => state.user.nickname,
    userInfo: state => state.user.info,
    resumeField: state => state.user.resumeField,
    multiTab: state => state.app.multiTab,
    hasGetInfo: state => state.user.hasGetInfo
}
export default getters
