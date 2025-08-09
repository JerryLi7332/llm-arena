const fs = require('fs');
const path = require('path');

// 复制目录的递归函数
function copyDir(src, dest) {
  // 创建目标目录
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  // 读取源目录
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// 主函数
function main() {
  const distPath = path.join(__dirname, '..', 'dist');
  const staticPath = path.join(__dirname, '..', '..', 'static');

  console.log('开始复制构建文件到后端static目录...');

  // 检查dist目录是否存在
  if (!fs.existsSync(distPath)) {
    console.error('错误: dist目录不存在，请先运行 npm run build');
    process.exit(1);
  }

  // 创建static目录
  if (!fs.existsSync(staticPath)) {
    fs.mkdirSync(staticPath, { recursive: true });
  }

  // 清空static目录
  if (fs.existsSync(staticPath)) {
    const staticEntries = fs.readdirSync(staticPath);
    for (let entry of staticEntries) {
      const entryPath = path.join(staticPath, entry);
      if (fs.lstatSync(entryPath).isDirectory()) {
        fs.rmSync(entryPath, { recursive: true, force: true });
      } else {
        fs.unlinkSync(entryPath);
      }
    }
  }

  // 复制文件
  copyDir(distPath, staticPath);

  console.log('构建文件已成功复制到 ../static/ 目录');
  console.log('现在可以启动后端服务来访问Vue应用');
}

// 运行主函数
main();
