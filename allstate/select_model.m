function select_model(xtrain,ytrain,xtest,ytest,xval,yval,label)
    fprintf('Running model selection for data %s\n',label);
    fprintf('xtrain: %dx%d\n',size(xtrain,1),size(xtrain,2));
    fprintf('ytrain: %dx%d\n',size(ytrain,1),size(ytrain,2));
    fprintf('xtest: %dx%d\n',size(xtest,1),size(xtest,2));
    fprintf('ytest: %dx%d\n',size(ytest,1),size(ytest,2));
    fprintf('xval: %dx%d\n',size(xval,1),size(xval,2));
    fprintf('yval: %dx%d\n',size(yval,1),size(yval,2));
    %fprintf('Press enter to train the neural network\n');
    %pause;
    hidden_vals=[1000];
    lambda_vals=[-3000 -10000 -30000 -100000];
    params=ones(size(hidden_vals,2)*size(lambda_vals,2),5)*1000;
    for i =1:size(hidden_vals,2)
        for j=1:size(lambda_vals,2)
            params((i-1)*size(lambda_vals,2) + j,1)=hidden_vals(i);
            params((i-1)*size(lambda_vals,2) + j,2)=lambda_vals(j);
        end
    end
     
    for i =1:size(params,1)
        fprintf('%s:model %d/%d\n',label,i,size(params,1));
        hiddenv=params(i,1);
        wp=params(i,2);
        nn=nnsetup([size(xtrain,2),100,size(ytrain,2)]);
        nn.activation_function = 'sigm'; %  Sigmoid activation function
        nn.output='softmax';
        nn.learningRate=1.5;
        nn.scaling_learningRate=1;
        opts.numepochs =  20;   %  Number of full sweeps through data
        opts.batchsize = size(xtrain,1);  %  Take a mean gradient step over this many samples
        opts.plot=0;
        nn.weightPenaltyL2=wp;
        [nn, L] = nntrain(nn, xtrain, ytrain, opts);
        [er, bad] = nntest(nn, xtrain, ytrain);
        params(i,3)=er;
        [er, bad] = nntest(nn, xval, yval);
        params(i,4)=er;
        [er, bad] = nntest(nn, xtest, ytest);
        params(i,5)=er;
        disp(params(i:i,:));
        [minv,imin]=min(params(:,4));
        disp(['The best params are : ' num2str(params(imin,:))]);
        if i==imin
            fprintf('Saving model...\n');
            save(strcat('model_',label),'nn');
        end
    end
    save(label, "params");
    [minv,imin]=min(params(:,4));
    disp(params);
    disp(['The best params are : ' num2str(params(imin,:))]);
    figure;
    scatter3(params(:,1),params(:,2),params(:,4));
end
