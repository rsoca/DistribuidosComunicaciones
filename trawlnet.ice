module TrawlNet {

  exception FileDoesNotExistError {
    string info;
  };

  interface Sender {
    string receive(int size);
    void close();
    void destroy();
  };

  interface Receiver {
    void start();
    void destroy();
  };

  sequence<Receiver*> ReceiversList;
  sequence<string> FileList;

  interface Transfer {
    ReceiversList createPeers(FileList files)
      throws FileDoesNotExistError;
    void destroyPeer(string peerId);
    void destroy();
  };

  struct PeerInfo {
    Transfer* transfer;
    string fileName;
  };

  interface SenderFactory {
    Sender* create(string fileName)
      throws FileDoesNotExistError;
  };

  interface ReceiverFactory {
    Receiver* create(string fileName, Sender* sender, Transfer* transfer);
  };

  interface TransferFactory {
    Transfer* newTransfer(ReceiverFactory* receiverFactory);
  };

  interface PeerEvent {
    void peerFinished(PeerInfo peerInfo);
  };

  interface TransferEvent {
    void transferFinished(Transfer* transfer);
  };
  
};
