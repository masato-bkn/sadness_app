export {trimCanvasToSquare, resizeCanvas}

/**
 * canvasを正方形にトリミングする
 */
function trimCanvasToSquare(canvas,image,faceLocation,canvasWidth,canvasHeight){
    const ctx = canvas.getContext("2d")

    let x = faceLocation.Left * image.width
    let y = faceLocation.Top * image.height
    let width = faceLocation.Width * image.width
    let height = faceLocation.Height * image.height

    // 正方形にリサイズ
    // 縦横,長い方にもう一方を合わせる
    if (width < height){
        width = height
    } else {
        height = width
    }

    // canvasの大きさを指定
    canvas.height = canvasWidth
    canvas.width = canvasHeight
    ctx.drawImage(image, x, y, width, height, 0, 0, canvasWidth, canvasHeight)
}

/**
 * canvasを縦横比を崩さずにリサイズ
*/
function resizeCanvas(canvas,image,canvasHeight) {
    const ctx = canvas.getContext("2d")

    // 画像を表示枠に収まるように縦横比を維持したままリサイズする。
    const maxHeight = 380
    const maxWidth = 420

    let dh // イメージを描画する幅
    let dw // イメージを描画する高さ

    // 縦幅が最大値を超えている場合
    if (image.height >= maxHeight) {
        // 縦比率にイメージの縦・横を合わせる
        dh = maxHeight
        dw = image.width * (dh / image.height)
        // canvasの大きさを指定
        canvas.width = dw
        canvas.height = dh

        // サムネイルに画像を描画
        ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, dw, dh)
    } 

    // 横幅が最大値を超えている場合    
    if (image.width >= maxWidth) {
        // 横比率にイメージの縦・横を合わせる
        dw = maxWidth
        dh = image.height * (maxWidth / image.width)

        // canvasの大きさを指定
        canvas.height = dh
        canvas.width = dw
        // サムネイルに画像を描画
        ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, dw, dh)
    }
    // どちらでもない場合は横に比率を合わせる
    if (image.width < maxWidth && image.height < maxHeight) {
        // 横比率にイメージの縦・横を合わせる
        dw = maxWidth
        dh = image.height * (maxWidth / image.width)

        // canvasの大きさを指定
        canvas.height = dh
        canvas.width = dw
        // サムネイルに画像を描画
        ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, dw, dh)
    }
}

