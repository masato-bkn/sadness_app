let DEBUG_MODE = process.env.DEBUG_MODE == 1 ? true : false;

// デバッグモードの場合にログを出力する
export default function(s) {
    if (DEBUG_MODE) {
        console.log(s);
    }
}