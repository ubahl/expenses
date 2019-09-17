build:
	sam build

package:
	sam package --template-file template.yaml --s3-bucket sam-bucket-2 --output-template-file packaged.yaml

deploy:
	sam deploy --template-file ./packaged.yaml --stack-name expensestack  --capabilities CAPABILITY_IAM

testdeploy:
	sam build
	sam package --template-file template.yaml --s3-bucket sam-bucket-2 --output-template-file packagedtest.yaml
	sam deploy --template-file ./packagedtest.yaml --stack-name expensestackTEST  --capabilities CAPABILITY_IAM