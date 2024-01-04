/**
 * Get all databases
 */

 const { CloudantV1 } = require("@ibm-cloud/cloudant");
 const { IamAuthenticator } = require("ibm-cloud-sdk-core");
 
 function main(params) {

  const cloudant = Cloudant({
      url: params.COUCH_URL,
      plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
  });

  let dbListPromise = getDbs(cloudant);
  return dbListPromise;
}
 
 function getDbs(cloudant) {
   cloudant
     .getAllDbs()
     .then((body) => {
       body.forEach((db) => {
         dbList.push(db);
       });
     })
     .catch((err) => {
       console.log(err);
     });
 }