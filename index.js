const fs = require('fs');
const path = require('path');
const inquirer = require('inquirer');
const open = require('open');
const readline = require('readline');
const chalk = require('chalk');

const logo = `
${chalk.green(`
 █████╗ ███████╗██╗███╗   ███╗████████╗
██╔══██╗██╔════╝██║████╗ ████║╚══██╔══╝
███████║███████╗██║██╔████╔██║   ██║
██╔══██║╚════██║██║██║╚██╔╝██║   ██║
██║  ██║███████║██║██║ ╚═╝ ██║   ██║
╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝   ╚═╝
----------------ASIMT----------------
ASIMT TOOLS TERMUX GRATIS YANG DI CIPTAKAN
OLEH ROOX UNTUK BUKA BLOKIR WHATSAPP/UNBAND

© 2025 rooxJSphire. All rights reserved.`)}
`;

async function main() {
  while (true) {
    console.clear();
    console.log(logo);

    const { menu } = await inquirer.prompt([
      {
        type: 'list',
        name: 'menu',
        message: chalk.cyan('Pilih Menu:'),
        choices: [
          { name: '1. Unban WhatsApp Biasa (Spam)', value: '1' },
          { name: '2. Unban WhatsApp Biasa (Permanent)', value: '2' },
          { name: '3. Unban WhatsApp Bisnis (Spam)', value: '3' },
          { name: '4. Unban WhatsApp Bisnis (Permanent)', value: '4' },
          '----------pembatas---------',
          { name: '5. Developer Info', value: 'dev' }
        ]
      }
    ]);

    if (menu === 'dev') {
      console.clear();
      console.log(chalk.yellow('\n👨‍💻 Developer Info:\n'));
      console.log(chalk.green('📞 Nomor     : 088991838060'));
      console.log(chalk.green('🎵 Tiktok    : tiktok.com/@rooxjsphire'));
      console.log(chalk.green('🔗 Informasi : https://whatsapp.com/channel/0029Vb6JTAHGJP8HbYcugb3p\n'));
      console.log(chalk.cyan('Ketik ') + chalk.bold.green('kembali') + chalk.cyan(' untuk balik ke menu utama.\n'));

      await waitCommand(['kembali']);
      continue;
    }

    const filePath = path.join(__dirname, 'mt', `${menu}.txt`);
    if (!fs.existsSync(filePath)) {
      console.log(chalk.red(`❌ File teks banding tidak ditemukan: ${filePath}`));
      return;
    }

    const teks = fs.readFileSync(filePath, 'utf-8');
    console.clear();
    console.log(logo);
    console.log('\n📄 ' + chalk.yellow('Berikut Teks Banding Anda:\n'));
    console.log(chalk.whiteBright(teks));

    console.log('\n✅ ' + chalk.cyan('Langkah-langkah Banding:'));
    console.log(chalk.white('1.') + ' Salin teks di atas secara manual.');
    console.log(chalk.white('2.') + ' Ketik command sesuai perintah di bawah.');
    console.log(chalk.white('3.') + ' Tempel teks & kirim permintaan.');
    console.log('\n📟 Ketik: ' + chalk.bold.green('lanjut') + chalk.white(' untuk membuka halaman support.'));
    console.log('📟 Atau ketik: ' + chalk.bold.green('kembali') + chalk.white(' untuk kembali ke menu.\n'));

    const cmd = await waitCommand(['lanjut', 'kembali']);
    if (cmd === 'lanjut') {
      console.log(chalk.yellow('🔁 Membuka halaman support WhatsApp...'));
      await open('https://wa.me/support');
      return;
    }
  }
}

function waitCommand(validCommands = []) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question(chalk.cyan('\nCommand > '), (cmd) => {
      rl.close();
      const lower = cmd.trim().toLowerCase();
      if (validCommands.includes(lower)) {
        resolve(lower);
      } else {
        console.log(chalk.red('\n❌ Command tidak dikenali. Ketik salah satu: ' + validCommands.join(' / ')));
        resolve(waitCommand(validCommands)); // tunggu ulang
      }
    });
  });
}

main();