import storage from '@/store/store'
import {DEFAULT_THEME,DEFAULT_LAYOUT,THEME_TYPE,LAYOUT_TYPE} from '@/store/constant'
const app={
    state:{
        theme:DEFAULT_THEME,
        layout:DEFAULT_LAYOUT
    },
    mutations:{
        SET_THEME:(state,theme)=>{
            state.theme=theme
            storage.set(THEME_TYPE,theme)
},
        SET_LAYOUT:(state,layout)=>{
            state.layout=layout
            storage.set(LAYOUT_TYPE,layout)
        },
    }
}

export default app
