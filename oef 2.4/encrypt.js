const fs = require('fs');
const kyber = require('crystals-kyber');


async function encryptCustomSentence(sentence) {
  
  let pk_sk = kyber.KeyGen768();
  let pk = pk_sk[0];  
  let sk = pk_sk[1];  


  let c_ss = kyber.Encrypt768(pk);
  let c = c_ss[0];    
  let ss1 = c_ss[1];  

  
  const encoder = new TextEncoder();
  const encodedMessage = encoder.encode(sentence); 

  function xorEncryptDecrypt(messageBytes, keyBytes) {
    const encrypted = new Uint8Array(messageBytes.length);
    for (let i = 0; i < messageBytes.length; i++) {
      encrypted[i] = messageBytes[i] ^ keyBytes[i % keyBytes.length]; 
    }
    return encrypted;
  }

  let encryptedMessage = xorEncryptDecrypt(encodedMessage, ss1);  
  console.log("Encrypted Message:", encryptedMessage);

  fs.writeFileSync('public_key.json', JSON.stringify(pk));
  fs.writeFileSync('ciphertext.json', JSON.stringify(c));
  fs.writeFileSync('encrypted_message.json', JSON.stringify(Array.from(encryptedMessage)));
  fs.writeFileSync('private_key.json', JSON.stringify(sk)); // Ook de private key opslaan

  console.log("Encryptie succesvol. Publieke sleutel, ciphertext en versleutelde zin opgeslagen.");
}

const sentence = "Dit is een post-quantum cryptografie test.";
encryptCustomSentence(sentence);
