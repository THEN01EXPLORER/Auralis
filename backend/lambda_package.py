"""
Script to create a Lambda deployment package without SAM CLI
"""
import os
import shutil
import zipfile

def create_lambda_package():
    """Create a deployment package for AWS Lambda"""
    
    # Create deployment directory
    deploy_dir = "lambda_deploy"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Copy app directory
    shutil.copytree("app", os.path.join(deploy_dir, "app"))
    
    # Install dependencies to deploy directory
    print("Installing dependencies...")
    os.system(f"pip install -r requirements.txt -t {deploy_dir}")
    
    # Create zip file
    print("Creating deployment package...")
    zip_path = "auralis_lambda.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n✅ Deployment package created: {zip_path}")
    print(f"📦 Size: {os.path.getsize(zip_path) / (1024*1024):.2f} MB")
    print("\nNext steps:")
    print("1. Go to AWS Lambda Console: https://console.aws.amazon.com/lambda/")
    print("2. Create new function (Python 3.11)")
    print("3. Upload auralis_lambda.zip")
    print("4. Set handler to: app.main.handler")
    print("5. Create API Gateway trigger")
    
    # Cleanup
    shutil.rmtree(deploy_dir)

if __name__ == "__main__":
    create_lambda_package()
