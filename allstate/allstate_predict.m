function y=allstate_predict(file,label,prefix)

    fprintf('Loading data...\n');
    load(file);
    fprintf('Data loaded!\n');
    fprintf('Adding path to DeepLearnToolbox\n');
    addpath(genpath('/home/coneptum/DeepLearnToolbox'));



    fprintf('Retrieving the model for %s\n',label);
    load(strcat('model_y_',label,'.mat'));
    fprintf('Retrieving mu and sigma for %s\n',label);
    load(strcat('mu_sigma_',label,'.mat'));
    fprintf('Normalizing\n');
    X=normalize(X(:,2:size(X,2)),mu,sigma);

    fprintf('Predicting\n');
    y=nnpredict(nn,X);
    fprintf('Saving results\n');
    save(strcat(prefix,label,'.mat') ,'y');

end

