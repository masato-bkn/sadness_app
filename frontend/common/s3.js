import { Promise, resolve, reject } from 'q';

export {uploadToS3}

// S3upload関数
function  uploadToS3(data, path, bucket){
    const aws = require("aws-sdk")
    const s3 = new aws.S3()

    const params = {
        Body: data,
        Bucket: bucket,
        Key: path, // TODO バケット/日付/ファイル名
    }

    aws.config.update({
        region: process.env.AWS_S3_REGION,
        secretAccessKey:process.env.AWS_SECRET_ACCESS_KEY,
        accessKeyId: process.env.AWS_ACCESS_KEY
    })
    return new Promise((resolve, reject)=>{
        s3.upload(params, (err, data) => {
            if(err){
                reject(err)
            } else {
                resolve(data)
            }
        })
    })
}