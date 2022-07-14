const crypto = require('crypto');
const moment = require('moment');
const jwt = require('jsonwebtoken');

const api_key = process.env.API_KEY || '';
const key_id = process.env.KEY_ID || '';
const aud_url = process.env.AUD_URL || '';

const printApiKey = async () => {

  if (!(api_key && key_id && aud_url)) {
    console.log(
      "One or more of the following environment variables are missing,","\n",
      "API_KEY","\n",
      "KEY_ID","\n",
      "AUD_URL","\n"
    );
    return;
  }

  // Prepare the derived signing key
  let hash = crypto.createHmac('sha512', api_key);
  hash.update(key_id);
  hash = hash.digest('base64');

  // JWT payload
  const payload = {
    metadata: {
      reason: 'fetch usages',
      requesterip: '127.0.0.1',
      'date-time': moment().toISOString(),
      'user-agent': 'curl'
    }
  };

  //JWT options
  const options = {
    audience: aud_url,
    issuer: key_id,
    algorithm: 'HS512',
    keyid: key_id,
    expiresIn: 300
  };

  //Sign JWT
  const token = jwt.sign(payload, hash, options);
  console.log("Token: ", token);
};

printApiKey();
