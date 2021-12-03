import * as fs from 'fs';

const num = process.argv[2]

const target = `${__dirname}`
const templates = `${target}/template`

function replace(input: string) : string {
    return input.replace('{{num}}', num)
}

fs.readdir(templates, function (err, files) {
    files.forEach(file => {
        const newFile = `${target}/${replace(file)}`
        console.log(`creating ${newFile}`)

        fs.copyFile(`${templates}/${file}`, newFile, () => {
            const content = fs.readFileSync(newFile, 'utf8')
            fs.writeFileSync(newFile, replace(content))
        })
    })
})
