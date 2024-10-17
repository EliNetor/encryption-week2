const fs = require('fs');
const kyber = require('crystals-kyber');

async function decryptCustomMessage() {
  let pk = JSON.parse(fs.readFileSync('public_key.json', 'utf8'));
  let sk = JSON.parse(fs.readFileSync('private_key.json', 'utf8'));
  let c = JSON.parse(fs.readFileSync('ciphertext.json', 'utf8'));
  let encryptedMessage = new Uint8Array(JSON.parse(fs.readFileSync('encrypted_message.json', 'utf8')));

  let ss2 = kyber.Decrypt768(c, sk);

  function xorEncryptDecrypt(messageBytes, keyBytes) {
    const decrypted = new Uint8Array(messageBytes.length);
    for (let i = 0; i < messageBytes.length; i++) {
      decrypted[i] = messageBytes[i] ^ keyBytes[i % keyBytes.length];
    }
    return decrypted;
  }

  let decryptedMessage = xorEncryptDecrypt(encryptedMessage, ss2);

  const decoder = new TextDecoder();
  const originalMessage = decoder.decode(decryptedMessage);

  console.log("Decrypted Message:", originalMessage);
}

decryptCustomMessage();
